from starception import install_error_handler
from starlette.applications import Starlette
from starlette_babel.translator import load_messages_from_directories
from {{cookiecutter.project_slug}}.config.errors import error_handlers
from {{cookiecutter.project_slug}}.config.middleware import middleware
from {{cookiecutter.project_slug}}.config.routes import routes
from {{cookiecutter.project_slug}}.config.settings import Settings, settings

install_error_handler()
load_messages_from_directories([settings.package_dir / "locales"])

def create_app(settings: Settings) -> Starlette:
    return Starlette(
        routes=routes,
        debug=settings.debug,
        middleware=middleware,
        exception_handlers=error_handlers,
    )


app = create_app(settings)
