import aiohttp
import inspect
import asyncio
import ssl
import logging
from .helpers import func_args
from ..Api import API
from aiohttp import web
from .parser import parser
from colorama import Fore, Style


class _WebHookError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def _log(response):
    if not response['ok']:
        logging.error(response)


class _Api(API):
    def __init__(self, token):
        super().__init__("https://api.telegram.org/bot")
        self.token = token
        self.file_download_url = "https://api.telegram.org/file/bot"
        with open('log.log', 'w'):
            pass
        logging.basicConfig(filename='log.log')

    async def _api_get(self, method: str, params: dict):
        url = self._api_url + self.token + method
        async with aiohttp.ClientSession() as session:
            r = await session.get(url, params=params)
            r = await r.json()
            _log(r)
            return r

    async def _api_post(self, method: str, params: dict, data: dict=None):
        url = self._api_url + self.token + method
        async with aiohttp.ClientSession() as session:
            r = await session.post(url, params=params, data=data)
            r = await r.json()
            _log(r)
            return r

    async def set_webhook(self, web_hook, cert=None):
        print("{}Setting webhook ...... {}".format(Fore.GREEN, Style.RESET_ALL))

        params = {'url': web_hook}
        data = {'certificate': cert} if cert is not None else None
        result = await self._api_post("/setWebhook", params, data=data)

        print("{}{}Status: [{}]\nDescription: [{}] {}"
              .format(Fore.GREEN, Fore.BLUE, str(result.get('ok', "")), result.get('description', ""), Style.RESET_ALL))

        if not result['ok']:
            raise _WebHookError(result)

    async def delete_webhook(self):
        print("{}Deleting webhook ......{}".format(Fore.GREEN, Style.RESET_ALL))
        result = await self._api_get("/deleteWebhook", params={})
        print("{}Status: [{}]\nDescription: [{}] {}"
              .format(Fore.BLUE, str(result.get('ok', "")), result.get('description', ""), Style.RESET_ALL))

    async def send_message(self, chat_id, text, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get("/sendMessage", params=params)
        return result

    async def answer_inline_query(self, answer_inline_query):
        result = await self._api_get("/answerInlineQuery", params=answer_inline_query)
        return result

    async def send_photo(self, chat_id, photo, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        data = {'photo': photo}
        result = await self._api_post("/sendPhoto", params, data)
        return result

    async def send_invoice(self, chat_id, title, payload, provider_token, start_parameter, currency, prices, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get('/sendInvoice', params)
        return result

    async def answer_precheckout_query(self, pre_checkout_query_id, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get('/answerPreCheckoutQuery', params)
        return result

    async def get_file(self, file_id):
        params = {'file_id': file_id}
        result = await self._api_get('/getFile', params)
        download_url = self.file_download_url + self.token + '/' + result['result']['file_path']
        async with aiohttp.ClientSession() as session:
            result = await session.get(download_url)
            result = await result.read()
        return result

    async def delete_message(self, chat_id, m_id):
        params = func_args(inspect.currentframe())
        result = await self._api_get('/deleteMessage', params)
        return result


class Bot:
    def __init__(self, config, loop=None):
        self._bot_url = config['bot_url']
        self._port = config['port']
        self._token = config['token']
        self._web_hook = config['web_hook']
        self._cert = config.get('cert', 0)
        self._keyfile = config.get('keyfile', 0)
        self._self_signed_certificate = None
        self.api = _Api(self._token)
        self.loop = loop

    async def _handler(self, update):
        json_update = await update.json()
        await self.handler(parser(json_update))
        return web.Response(text="OK")

    async def handler(self, update):
        raise NotImplementedError("Please Implement this method")

    def _create_ssl_context(self):
        if self._cert and self._keyfile:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=self._cert, keyfile=self._keyfile)
            return context
        else:
            return None

    async def run(self):
        app = web.Application()
        app.router.add_post('/', self._handler)
        handler = app.make_handler()
        ssl_context = self._create_ssl_context()
        serv = await self.loop.create_server(handler, self._bot_url, self._port, ssl=ssl_context)
        print("{}Bot run on {}[{}:{}]{}\n"
              .format(Fore.GREEN, Fore.BLUE, self._bot_url, str(self._port), Style.RESET_ALL))
        return serv
