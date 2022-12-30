from kupala.routing import include
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from {{cookiecutter.project_slug}}.config.settings import settings

routes = [
    *include('{{cookiecutter.project_slug}}.views'),
    Mount("/static", app=StaticFiles(packages=[settings.package_name]), name="static"),
]
