import dataclasses
import importlib
import os
import sys
import typing
from pathlib import Path

from kupala.config import Secrets
from starlette.config import Config

package_name = __name__.split(".")[0]
package_root = Path(str(importlib.import_module(package_name).__file__)).parent
project_root = package_root.parent

env_file = project_root / ".env"
env = Config(env_file)

IS_TESTING = "pytest" in sys.argv[0]
ENV = env("ENV", default="test" if IS_TESTING else "production")
SECRETS_DIR = {"local": "_local/secrets"}.get(ENV, "/run/secrets")

secret = Secrets(SECRETS_DIR)


@dataclasses.dataclass
class AppSettings:
    secret_key: str = env("SECRET_KEY", default=secret("secret_key.secret", ""))
    debug: bool = env("DEBUG", cast=bool, default=False)
    environment: str = ENV
    base_url: str = env("BASE_URL", default="http://localhost:8000")
    app_name: str = "{{ cookiecutter.project_name }}"
    project_root: Path = project_root
    package_dir: Path = package_root
    package_name: str = package_name
    upload_dir: str | os.PathLike = project_root / "uploads"


@dataclasses.dataclass
class ReleaseSettings:
    release_id: str = env("RELEASE_ID", default="")


@dataclasses.dataclass
class SecuritySettings:
    trusted_hosts: list[str] = dataclasses.field(default_factory=lambda: ["*"])


@dataclasses.dataclass
class SessionSettings:
    lifetime: int = 3600 * 24


@dataclasses.dataclass
class Settings(AppSettings):
    release = ReleaseSettings()
    security = SecuritySettings()
    session = SessionSettings()


def new_settings(**overrides: typing.Any) -> Settings:
    return Settings(**overrides)


def new_settings_for_test() -> Settings:
    return new_settings(
        debug=True,
        environment="test",
    )


settings = new_settings_for_test() if IS_TESTING else new_settings()


def get_settings() -> Settings:
    """Get current application settings."""
    return settings
