from litestar import Controller, get
from litestar.response import Template


class SessionController(Controller):
    path = "/"

    @get(path=["/login"])
    async def get_login_view(self) -> Template:
        return Template(template_name="session/login.html.jinja")
    