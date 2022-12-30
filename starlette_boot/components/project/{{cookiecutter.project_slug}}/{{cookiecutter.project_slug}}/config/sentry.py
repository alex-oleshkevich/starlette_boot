import sentry_sdk
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from {{cookiecutter.project_slug}}.config.settings import settings


def setup_sentry() -> None:
    if settings.sentry.dsn:
        sentry_sdk.init(
            settings.sentry.dsn,
            traces_sample_rate=settings.sentry.traces_sample_rate,
            environment=settings.environment,
            release=settings.release.release_id,
            integrations=[
                StarletteIntegration(),
                HttpxIntegration(),
            ],
        )
