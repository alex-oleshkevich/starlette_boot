import datetime

from kupala.routing import Routes
from starlette.requests import Request
from starlette.responses import JSONResponse

from {{cookiecutter.project_slug}}.config.settings import settings

BOOT_TIME = datetime.datetime.now()
routes = Routes()


@routes("/health")
async def healthcheck_view(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


@routes.route("/version")
async def version_view(request: Request) -> JSONResponse:
    """Privacy Policy page."""
    return JSONResponse(
        {
            "env": settings.environment,
            "debug": settings.debug,
            "release_id": settings.release.release_id,
            "branch": settings.release.branch,
            "commit": settings.release.commit,
            "build_date": settings.release.build_date,
            "boot_time": BOOT_TIME.isoformat(),
        }
    )
