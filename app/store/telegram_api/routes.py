import typing



if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_te_routes(app: "Application"):
    from app.admin.views import AdminLoginView
    url_webhook = "/API/web" + str(app.config.bot.token)
    app.router.add_view(url_webhook, Webhook_handling)


