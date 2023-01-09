import pytest

from main import create_app


@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client