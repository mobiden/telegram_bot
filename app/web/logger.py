import logging
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_logging(_: "Application") -> None:

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG) # TODO: to change later
