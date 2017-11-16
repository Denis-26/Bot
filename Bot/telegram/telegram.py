import aiohttp
import io
import inspect
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


class _Api(API):
    def __init__(self, token):
        super().__init__("https://api.telegram.org/bot")
        self.token = token
        self.file_download_url = "https://api.telegram.org/file/bot"
        with open('log.log', 'w') as log_file: pass
        logging.basicConfig(filename = 'log.log')

    def _log(self, response):
        if not response['ok']:
            logging.error(response)

    async def _api_get(self, method: str, params: dict):
        url = self._api_url + self.token + method
        async with aiohttp.ClientSession() as session:
            r = await session.get(url, params=params)
            r = await r.json()
            self._log(r)
            return r

    async def _api_post(self, method: str, params: dict, data: dict):
        url = self._api_url + self.token + method
        async with aiohttp.ClientSession() as session:
            r = await session.post(url, params=params, data=data)
            r = await r.json()
            self._log(r)
            return r

    async def set_webhook(self, web_hook, cert=None):
        print("{}Setting webhook ...... {}".format(Fore.GREEN, Style.RESET_ALL))
        if cert is not None:
            params = {'url': web_hook}
            data = {'certificate': cert}
            result = await self._api_post("/setWebhook", params, data)
        else:
            params = {'url': web_hook}
            result = await self._api_get("/setWebhook", params)
        print("{}Webhook ...... {} [{}] {}".format(Fore.GREEN, Fore.BLUE, str(result['ok']), Style.RESET_ALL))
        if result['ok']:
            return result
        raise _WebHookError(result)

    async def delete_webhook(self):
        result = await self._api_get("/deleteWebhook")
        self._log(result)

    async def send_message(self, chat_id, text, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get("/sendMessage", params=params)
        self._log(result)
        return result

    async def answer_inline_query(self, answer_inline_query):
        result = await self._api_get("/answerInlineQuery", params=answer_inline_query)
        self._log(result)
        return result

    async def send_photo(self, chat_id, photo, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        data = {'photo': photo}
        result = self._api_post("/sendPhoto", params, data)
        self._log(result)
        return result

    async def send_invoice(self, chat_id, title, payload, provider_token, start_parameter, currency, prices, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get('/sendInvoice', params)
        self._log(result)
        return result

    async def answer_precheckout_query(self, pre_checkout_query_id, **kwargs):
        argvalues = func_args(inspect.currentframe())
        params = {**argvalues, **kwargs}
        result = await self._api_get('/answerPreCheckoutQuery', params)
        self._log(result)
        return result

    async def get_file(self, file_id):
        params = {'file_id': file_id}
        result = await self._api_get('/getFile', params)
        self._log(result)
        download_url = self.file_download_url + self.token + '/' + result['result']['file_path']
        async with aiohttp.ClientSession() as session:
            result = await session.get(download_url)
            result = await result.read()
            result = io.BytesIO(result)
        return result

    async def delete_message(self, chat_id, m_id):
        params = func_args(inspect.currentframe())
        result = await self._api_get('/deleteMessage', params)
        self._log(result)
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

    def set_self_signed_certificate(self, cert_pem):
        self._self_signed_certificate = cert_pem

    def run(self):
        app = web.Application()
        app.router.add_post('/', self._handler)
        handler = app.make_handler()
        ssl_context = self._create_ssl_context()
        server = self.loop.create_server(handler, self._bot_url, self._port, ssl=ssl_context)
        self.loop.run_until_complete(server)
        self.loop.run_until_complete(self.api.set_webhook(self._web_hook, self._self_signed_certificate))

        print("{}Bot run on {}[{}:{}]{}\n".format(Fore.GREEN, Fore.BLUE, self._bot_url, str(self._port), Style.RESET_ALL))
