import asyncio
import aiohttp


class API:
    def __init__(self, url):
        self._api_url = url

    async def send_message(self, chat_id, text, **kwargs):
        raise NotImplementedError("Please Implement this method")

    async def send_photo(self, chat_id, photo, **kwargs):
        raise NotImplementedError("Please Implement this method")
