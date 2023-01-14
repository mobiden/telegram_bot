import os

from app.web.app import app

from aiohttp.web import run_app

from my_logging import create_logs



def create_app():
    from app.web.app import setup_app
    return setup_app(config_path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'config.yml'))

#application = app

if __name__ == "__main__":
    create_logs('main start')
    run_app(create_app(), port=8080)

