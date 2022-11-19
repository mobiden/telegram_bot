import json

import typing
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.telegram_api.te_dataclasses import OutMessage

from app.store.telegram_api.te_poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

# TODO: перекинуть в конфиги
API_PATH = "https://api.telegram.org/bot"


class TelegramApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.up_id: Optional[int] = 0

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.poller = Poller(app.store)
        self.logger.info("start telegram polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()


    @staticmethod
    def _build_query(host: str, token: str, method: str, params: Optional [dict] = None) -> str:
        url = host + token + '/' + method
        if params:
            url += '?'
            url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url


    async def poll(self):
        te_poll_url = self._build_query(
                host=API_PATH,
                method='getUpdates',
                token=self.app.config.bot.token,
                params={
                    'offset': str(int(self.up_id) + 1),
                    'timeout': 5,
                        }
            )

        async with self.session.get(te_poll_url) as resp:
            data = await resp.json()
            if 'ok' in data:
                updates = data['result']

            if updates:
                ans = await self.app.store.bots_manager.handle_updates(updates)
                return ans


    async def send_message(self, message: OutMessage): # -> None:

        keyb = json.dumps(message.reply_markup)
        data = {'chat_id': message.chat_id, 'text': 'hellloooo',
                'parse_mode': 'HTML', 'reply_markup': keyb}
        send_url = self._build_query(
                host=API_PATH,
                token=self.app.config.bot.token,
                method="sendMessage",
                params={
                    'chat_id': message.chat_id,
                    'text': message.text

                },
            )
        async with self.session.post(url=send_url, json=data) as resp:
            data = await resp.json()
        return data

