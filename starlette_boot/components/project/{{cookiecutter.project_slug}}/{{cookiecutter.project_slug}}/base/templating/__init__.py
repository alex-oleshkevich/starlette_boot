import typing

from jinja2.runtime import Macro
from kupala.templating import Jinja2Templates
from starlette_flash.flash import flash_processor
from {{cookiecutter.project_slug}}.base.templating.factories import new_jinja_env
from {{cookiecutter.project_slug}}.base.templating.processors import project_context_processor
from {{cookiecutter.project_slug}}.config.settings import settings

context_processors = [
    flash_processor,
    project_context_processor,
]
jinja_env = new_jinja_env(settings)
templates = Jinja2Templates(jinja_env, context_processors=context_processors)


def render_to_string(template_name: str, context: typing.Mapping[str, typing.Any]) -> str:
    template = jinja_env.get_template(template_name)
    return template.render(context)


def macro(template_name: str, macro_name: str) -> Macro:
    template = jinja_env.get_template(template_name)
    return getattr(template.module, macro_name)
