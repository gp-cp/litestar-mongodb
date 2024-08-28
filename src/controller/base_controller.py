

from litestar import Controller, get
from litestar.response import Template


class BaseController(Controller):
    path = "/"

    @get(path=[""])
    async def index(self) -> Template:
        return Template(template_name="index.html.jinja")