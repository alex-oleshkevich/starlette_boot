import copy
import dataclasses
import os
import re
import time
import typing

from kupala.routing import Routes
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Host, Match, Mount, Route
from starlette.types import ASGIApp, Message, Receive, Scope, Send

routes = Routes()

request_counter = Counter(
    "starlette_requests",
    "Total count of requests processed.",
    ["method", "scheme", "endpoint", "path_name", "path_pattern"],
)

response_counter = Counter(
    "starlette_responses",
    "Total count of responses processed.",
    ["method", "scheme", "endpoint", "path_name", "path_pattern", "status_code"],
)

response_size = Gauge(
    "starlette_response_size",
    "Total size of responses processed, in bytes.",
    ["method", "scheme", "endpoint", "path_name", "path_pattern", "status_code"],
)

request_timing = Histogram(
    "starlette_request_timing",
    "Histogram of request processing time (seconds).",
    ["method", "scheme", "endpoint", "path_name", "path_pattern"],
)

exception_counter = Counter(
    "starlette_exceptions",
    "Total count of exceptions raised during request lifecycle.",
    ["method", "scheme", "endpoint", "path_name", "path_pattern", "exception_type"],
)


def get_fqname(obj: typing.Any) -> str:
    module_name = getattr(obj, "__module__", "<unknown module>")
    base_name = getattr(obj, "__name__", "<unknown callable>")
    return f"{module_name}.{base_name}"


@dataclasses.dataclass
class RouteMatch:
    endpoint: typing.Callable
    path_name: str = ""
    path_pattern: str = ""

    @property
    def endpoint_name(self) -> str:
        return get_fqname(self.endpoint)


def find_matched_route(scope: Scope, routes: typing.Iterable[BaseRoute]) -> RouteMatch | None:
    for route in routes:
        if isinstance(route, (Mount, Host)):
            mount_match, child_scope = route.matches(scope)
            if mount_match == Match.FULL:
                scope.update(child_scope)
                if route_match := find_matched_route(scope, route.routes):
                    return route_match
        elif isinstance(route, Route):
            match, child_scope = route.matches(scope)
            if match == Match.FULL:
                return RouteMatch(
                    endpoint=route.endpoint,
                    path_name=route.name,
                    path_pattern=route.path_format,
                )
    return None


def is_ignored(path: str, paths: list[str | re.Pattern]) -> bool:
    for exclusion in paths:
        if isinstance(exclusion, re.Pattern):
            return exclusion.match(path) is not None
        elif path in paths:
            return True
    return False


class MetricsMiddleware:
    def __init__(self, app: ASGIApp, exclude: list[str | re.Pattern] | None = None) -> None:
        self.app = app
        self.exclude = exclude or []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or is_ignored(scope["path"], self.exclude):
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        scheme = scope["scheme"]

        scope_copy = copy.copy(scope)
        route_match = find_matched_route(scope_copy, scope["app"].routes)
        if not route_match:
            await self.app(scope, receive, send)
            return

        labels = dict(
            method=method,
            scheme=scheme,
            path_name=route_match.path_name,
            path_pattern=route_match.path_pattern,
            endpoint=route_match.endpoint_name,
        )

        response_body_size = 0

        async def send_wrapper(message: Message) -> None:
            nonlocal response_body_size
            status_code = 0

            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_counter.labels(status_code=status_code, **labels).inc()

            if message["type"] == "http.response.body":
                response_body_size += len(message["body"])
                if not message.get("more_body", False):
                    response_size.labels(status_code=status_code, **labels).set(response_body_size)

            await send(message)

        start_time = time.perf_counter()
        try:
            request_counter.labels(**labels).inc()
            await self.app(scope, receive, send_wrapper)
        except Exception as ex:
            exception_counter.labels(exception_type=get_fqname(ex.__class__), **labels).inc()
            raise ex from None
        finally:
            time_taken = time.perf_counter() - start_time
            request_timing.labels(**labels).observe(time_taken)


@routes("/metrics")
async def metrics_view(request: Request) -> Response:
    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), headers={"Content-Type": CONTENT_TYPE_LATEST})
