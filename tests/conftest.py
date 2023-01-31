import os

import pytest
from app.web.app import setup_app


@pytest.fixture
def app():
    app = setup_app(
        config_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_config.yml")
    )
    return app


@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client
