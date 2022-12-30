from kupala.routing import Routes
from starlette.requests import Request
from starlette.responses import Response
from starlette_babel import gettext_lazy as _
from {{cookiecutter.project_slug}}.base.templating import templates

routes = Routes()


@routes.route("/", name="home")
async def index_view(request: Request) -> Response:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "page_title": _("Starlette application"),
        },
    )
