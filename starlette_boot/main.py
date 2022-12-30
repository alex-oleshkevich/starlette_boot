import click
import pathlib
import questionary
import sys
from cookiecutter.generate import generate_files
from slugify import slugify

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

    template_dir = pathlib.Path(__file__).parent / "templates" / "project"

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
def add() -> None:
    ...
