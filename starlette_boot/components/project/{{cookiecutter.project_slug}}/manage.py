#!/usr/bin/env python
import logging

from {{cookiecutter.project_slug}}.console import cli

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s")

if __name__ == "__main__":
    cli()
