import os
from unittest.mock import patch, AsyncMock, MagicMock, create_autospec, Mock

import aiohttp
import pytest
import requests

from aiohttp import ClientSession
from aioresponses import aioresponses

from app.store import Store


from app.store.telegram_api.te_poller import Poller
from app.web.app import setup_app


@pytest.fixture(autouse=True)
# перехватывает и отключает внешние сетевые вызовы, вызывает ошибку
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
  #      return {}
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())
    monkeypatch.setattr(ClientSession, "get", lambda *args, **kwargs: stunted_get())
    monkeypatch.setattr(ClientSession, "post", lambda *args, **kwargs: stunted_get())


# перехватывает вызовы кроме указанного.

@pytest.fixture(scope='session')
def api_telegram_off():
    with aioresponses(passthrough=["http://127.0.0.1"]) as responses_mock:
        responses_mock.post(
        'https://api.telegram.org/bot5407718698:AAF9BdK0PZetZcmqov9H93w06a-V89m2_-0/deleteWebhook',
            status=200,
            payload={'ok': True, 'result': True, 'description': 'Webhook is already deleted'},
                            )

        responses_mock.get(
        'https://api.telegram.org/bot5407718698:AAF9BdK0PZetZcmqov9H93w06a-V89m2_-0/getUpdates?offset=1&timeout=5',
            status=200,
            payload={'ok': True, 'result': []},
        )
    yield



@pytest.fixture()
def app_without_tel_api():
    TelegramApiAccessor = AsyncMock()
    app = setup_app(
        config_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_config.yml")
    )

    for item in app.on_startup:
        if 'TelegramApiAccessor' in str(item):
            app.on_startup.remove(item)
            item = AsyncMock()
    return app

# создает клиента
@pytest.fixture()
async def cli_without_tel_api(aiohttp_client, app_without_tel_api):

    client = await aiohttp_client(app_without_tel_api)
    yield client
