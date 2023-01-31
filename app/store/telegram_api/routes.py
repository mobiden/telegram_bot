import typing


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_te_routes(app: "Application"):
    from app.store.telegram_api.te_view import Webhook_handling

    url_webhook = "/API/web/" + str(app.config.bot.bot_token)
    app.router.add_view(url_webhook, Webhook_handling)
