import typing

from app.garden.views import FloraTypeAddView, FloraNameAddView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/flora.name_add", FloraNameAddView)
    app.router.add_view("/flora.type_add", FloraTypeAddView)
