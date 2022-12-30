import glob

import jinja2
from {{cookiecutter.project_slug}}.base.templating.library import library
from {{cookiecutter.project_slug}}.config.settings import Settings


def new_jinja_env(settings: Settings) -> jinja2.Environment:
    """Create a new Jinja2 environment."""
    jinja_env = jinja2.Environment(
        autoescape=True,
        loader=jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader(
                    [
                        *glob.glob(f"{settings.package_dir}/*/templates"),
                        settings.package_dir / "templates",
                    ]
                ),
                jinja2.PackageLoader("starlette_flash"),
            ]
        ),
    )
    jinja_env.globals.update({})
    jinja_env.filters.update(library.filters)

    return jinja_env
