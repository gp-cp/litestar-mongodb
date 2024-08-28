from litestar import Litestar, Router

from .base_controller import BaseController
from .session_controller import SessionController


def register_controller(handler: Litestar) -> None:
    handler.register(
        Router(
            path="",
            route_handlers=[BaseController, SessionController],
        )
    )
