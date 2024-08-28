from typing import Annotated

from litestar import Controller, Request, get, post
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Template

from schemas.user_schema import UserLoginSchema


class SessionController(Controller):
    path = "/"

    @get(path=["/login"], exclude_from_auth=True)
    async def get_login_view(self) -> Template:
        return Template(template_name="session/login.html.jinja", context={"title": "Login"})

    @post(path=["/login"], exclude_from_auth=True)
    async def login(
        self,
        request: Request,
        data: Annotated[
            UserLoginSchema,
            Body(media_type=RequestEncodingType.URL_ENCODED),
        ],
    ) -> dict:
        request.set_session({"user": data.email})

        return {"message": "Login successful"}
