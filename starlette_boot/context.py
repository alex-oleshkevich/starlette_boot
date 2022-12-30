import dataclasses

import pathlib
import typing


@dataclasses.dataclass
class Dependency:
    package_name: str
    version_spec: str
    group: str

    @property
    def spec(self) -> str:
        if self.version_spec == "*":
            return self.package_name
        return f"{self.package_name}@{self.version_spec}"


@dataclasses.dataclass
class Context:
    package_name: str
    pyproject: dict
    project_dir: pathlib.Path

    dependencies: list[Dependency] = dataclasses.field(default_factory=list)
    variables: dict[str, typing.Any] = dataclasses.field(default_factory=dict)

    def add_dependency(self, package_name: str, version_spec: str, group: str = "") -> None:
        self.dependencies.append(Dependency(package_name=package_name, version_spec=version_spec, group=group))

    def add_variables(self, variables: dict[str, typing.Any]) -> None:
        self.variables.update(variables)
