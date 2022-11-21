from aiohttp.web_app import Application



def setup_routes(app: Application):
    from app.admin.routes import setup_routes as admin_setup_routes
    from app.garden.routes import setup_routes as garden_setup_routes
    from app.store.telegram_api.routes import setup_te_routes as telegram_setup_routes

    admin_setup_routes(app)
    garden_setup_routes(app)
    telegram_setup_routes(app)