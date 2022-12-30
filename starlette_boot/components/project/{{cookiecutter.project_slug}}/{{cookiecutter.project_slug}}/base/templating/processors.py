import functools
import time
import typing

from starlette.datastructures import URL
from starlette.requests import Request

_boot_time = time.time()


def is_current(
    request: Request, path_name: str, path_params: dict[str, str | int] | None = None, exact: bool = False
) -> bool:
    """
    Test if current URL is the same as generated.

    By default, it checks if both URLs starts with the same prefix. When `exact` is True then both values must be equal.
    """
    target_url = request.app.router.url_path_for(path_name, **(path_params or {}))
    if exact:
        return target_url == request.url.path
    return target_url in request.url.path


def media_url(request: Request, path: str, path_name: str = "media") -> str:
    """Generates URL to an uploaded file."""
    if any([path.startswith("http://"), path.startswith("https://")]):
        return path
    return request.app.router.url_path_for(path_name, path=path)


def static_url(request: Request, path: str, path_name: str = "static", append_timestamp: bool = True) -> str:
    """Generates URL to a static file."""
    url = URL(request.app.router.url_path_for(path_name, path=path))
    if append_timestamp:
        url = url.include_query_params(ts=_boot_time)
    return str(url)


def url_for(request: Request, path_name: str, **path_params: typing.Any) -> URL:
    """Generates relative URL."""
    url = request.app.router.url_path_for(path_name, **path_params)
    return URL(url)


def abs_url_for(request: Request, path_name: str, **path_params: typing.Any) -> URL:
    """Generates absolute URL."""
    return URL(request.url_for(path_name, **path_params))


def project_context_processor(request: Request) -> dict[str, typing.Any]:
    return {
        "is_current": functools.partial(is_current, request),
        "app": request.app,
        "url": functools.partial(url_for, request),
        "abs_url": functools.partial(abs_url_for, request),
        "static_url": functools.partial(static_url, request),
        "media_url": functools.partial(media_url, request),
    }
