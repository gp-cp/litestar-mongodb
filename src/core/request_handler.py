from typing import Any

from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.connection import ASGIConnection
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.exceptions import NotFoundException
from litestar.middleware.session.server_side import (
    ServerSideSessionBackend,
    ServerSideSessionConfig,
)
from litestar.response import Redirect
from litestar.security.session_auth import SessionAuth
from litestar.static_files import StaticFilesConfig
from litestar.stores.redis import RedisStore
from litestar.template import TemplateConfig

from .mongo import get_mongo_context
from .settings import settings

REDIS_STORE = RedisStore.with_client(url=settings.REDIS_URL)


async def retrieve_user_handler(
    session: dict[str, Any],
    _: ASGIConnection,
) -> str | None:
    return session.get("user")


session_auth = SessionAuth[str, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=ServerSideSessionConfig(key="session"),
    exclude=["/static"],
)


def not_found_handler(_, __) -> Redirect:
    return Redirect(path="/not-found")


def new_request_handler(startup_events: list) -> Litestar:
    return Litestar(
        debug=True,
        cors_config=CORSConfig(
            allow_origins=["http://localhost:8000"],
            allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
            allow_credentials=True,
        ),
        compression_config=CompressionConfig(
            backend="brotli",
            brotli_gzip_fallback=True,
        ),
        on_startup=startup_events,
        template_config=TemplateConfig(
            directory=settings.TEMPLATE_DIR,
            engine=JinjaTemplateEngine,
        ),
        static_files_config=[
            StaticFilesConfig(
                directories=[settings.STATIC_DIR],
                path="/static",
            ),
        ],
        on_app_init=[session_auth.on_app_init],
        stores={
            "sessions": REDIS_STORE.with_namespace("session"),
        },
        dependencies={"mongo_context": get_mongo_context},
        exception_handlers={
            NotFoundException: not_found_handler,
        },
    )
