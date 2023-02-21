import os
from hashlib import sha256
from unittest.mock import patch, AsyncMock, MagicMock, create_autospec, Mock

import aiohttp
import pytest
import requests

from aiohttp import ClientSession
from aioresponses import aioresponses

from app.admin.models import AdminModel, Admin_Session
from app.store import Store



from app.web.app import setup_app
from app.web.utils import now


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

    async with client.app.database.db_async_session() as session:
        #TODO: извлекать таблицы из базы автоматически
        for table in ['admins', 'admin_sessions', 'users',
                      'flora_types', 'floras', 'garden_operations']:
            await session.execute(f'''TRUNCATE TABLE {table} CASCADE''')
        await session.commit()
    yield client
    async with client.app.database.db_async_session() as session:
        for table in ['admins', 'admin_sessions', 'users',
                      'flora_types', 'floras', 'garden_operations']:
            await session.execute(f'''TRUNCATE TABLE {table} CASCADE''')
        await session.commit()



@pytest.fixture
async def admin(app_without_tel_api):
    temp_admin:AdminModel = await app_without_tel_api.store.admins.create_admin(
        email="test@test.te", password="1234")

    return temp_admin


class authenticate:
    def __init__(self, cli, admin:AdminModel):
        self.cli = cli
        self.admin = admin

    async def __aenter__(self):
        session:Admin_Session = await self.cli.app.store.admins._create_admin_session(admin_id=self.admin.id)
        self.cli.session._default_headers["Authorization"] = f"Bearer {session.adm_sess_token}"

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.cli.session._default_headers.pop("Authorization")