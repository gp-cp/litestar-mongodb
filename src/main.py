from litestar import Litestar

from core.mongo import mongo_health_check
from core.request_handler import new_request_handler

from .controller import register_controller


def new_app() -> Litestar:
    handler = new_request_handler([mongo_health_check])
    register_controller(handler)
    return handler


app = new_app()
