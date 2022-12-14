import typing

from app.store.database.database import Database


if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.bot.manager import BotManager
        from app.store.admin.admin_accessor import AdminAccessor
        from app.store.store_flora.accessor import FloraAccessor
        from app.store.telegram_api.te_accessor import TelegramApiAccessor

        self.admins = AdminAccessor(app)
        self.telegram_api = TelegramApiAccessor(app)
        self.bots_manager = BotManager(app)
        self.store_flora = FloraAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.store = Store(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
