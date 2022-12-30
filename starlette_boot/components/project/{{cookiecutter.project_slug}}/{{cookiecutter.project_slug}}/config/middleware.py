from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starsessions import CookieStore, SessionAutoloadMiddleware, SessionMiddleware
from {{cookiecutter.project_slug}}.config.settings import settings

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=settings.security.trusted_hosts),
    Middleware(
        SessionMiddleware,
        rolling=True,
        cookie_https_only=settings.environment != "test",
        lifetime=settings.session.lifetime,
        cookie_path="/",
        store=CookieStore(secret_key=settings.secret_key),
    ),
    Middleware(SessionAutoloadMiddleware),
]
