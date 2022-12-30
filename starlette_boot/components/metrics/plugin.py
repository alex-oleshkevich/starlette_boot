from starlette_boot.context import Context


def configure(context: Context) -> None:
    context.add_dependency('prometheus-client', '*')
