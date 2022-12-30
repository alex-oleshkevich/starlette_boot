import asyncio
import typing
from asyncio import get_event_loop

import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient
from starlette_babel import switch_locale, switch_timezone
from {{cookiecutter.project_slug}}.config.settings import Settings, get_settings
from {{cookiecutter.project_slug}}.main import create_app


@pytest.fixture(scope="session")
def event_loop() -> typing.Generator[asyncio.AbstractEventLoop, None, None]:
    yield get_event_loop()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def app(settings: Settings) -> Starlette:
    return create_app(settings)


@pytest.fixture(scope="session")
def client(app: Starlette) -> typing.Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def auth_client(app: Starlette) -> typing.Generator[TestClient, None, None]:
    with TestClient(app) as client:
        client.cookies.clear()
        yield client

@pytest.fixture(scope="session", autouse=True)
def force_locale() -> typing.Generator[None, None, None]:
    with switch_locale("en"), switch_timezone("utc"):
        yield
