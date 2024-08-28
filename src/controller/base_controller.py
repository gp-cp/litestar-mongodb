from litestar import Controller, get
from litestar.response import Template


class BaseController(Controller):
    path = "/"

    @get(path=[""], exclude_from_auth=True)
    async def index(self) -> Template:
        return Template(template_name="index.html.jinja", context={"title": "Home"})

    @get(path=["/not-found"], exclude_from_auth=True)
    async def not_found(self) -> Template:
        return Template(template_name="not_found.html.jinja", context={"title": "Not found"})
