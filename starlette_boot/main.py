import click
import importlib
import os
import pathlib
import questionary
import subprocess
import sys
import tomli
from cookiecutter.generate import generate_files
from slugify import slugify

from starlette_boot.context import Context

PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11"]
DEFAULT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"

app = click.Group()


@app.command()  # type: ignore[misc]
@click.argument("directory")  # type: ignore[misc]
def new(directory: str) -> None:
    project_name = questionary.text("Project name").ask()
    variables = questionary.form(
        project_slug=questionary.text("Package name", default=slugify(project_name)),
        python_version=questionary.select(
            "Python version",
            default=DEFAULT_PYTHON_VERSION,
            choices=PYTHON_VERSIONS,
        ),
    ).ask()

    template_dir = pathlib.Path(__file__).parent / "components" / "project"

    generate_files(
        repo_dir=template_dir,
        context={
            "cookiecutter": {
                "project_name": project_name,
                "_copy_without_render": [
                    "*.html",
                ],
                **variables,
            }
        },
        overwrite_if_exists=True,
        output_dir=directory,
    )


@app.command()  # type: ignore[misc]
@click.argument("component")
def add(component: str) -> None:
    # find pyproject.toml file
    cwd = pathlib.Path(os.getcwd())
    pyproject = cwd / "pyproject.toml"
    if not pyproject.exists():
        click.secho("No pyproject.toml found in current directory nor in parents.", fg="red")
        raise click.Abort()

    # retrieve package name
    meta = tomli.load(pyproject.open("rb"))
    package_name = meta["tool"]["poetry"]["name"]

    click.secho(
        "Adding {component} into {project} project.".format(
            component=click.style(component, fg="cyan"),
            project=click.style(package_name, fg="cyan"),
        )
    )

    module_dir = cwd
    component_dir = pathlib.Path(__file__).parent / "components" / component
    plugin_module = importlib.import_module(f"starlette_boot.components.{component}.plugin")
    context = Context(package_name=package_name, project_dir=module_dir, pyproject=meta)
    plugin = getattr(plugin_module, "configure")
    plugin(context)

    generate_files(
        repo_dir=component_dir,
        context={
            "cookiecutter": {
                "project_slug": package_name,
                **context.variables,
                "_copy_without_render": [
                    "*.html",
                ],
            }
        },
        overwrite_if_exists=True,
        output_dir=module_dir,
    )

    if context.dependencies:
        dependencies = [dep.spec for dep in context.dependencies]
        dependencies_output = ", ".join([click.style(dep, fg="cyan") for dep in dependencies])
        click.echo(f"Installing {dependencies_output}")
        subprocess.call(["poetry", "add", "--lock", " ".join(dependencies)])

    subprocess.call(["black", "."])
