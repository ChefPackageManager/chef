from typing import Any

from chef.cli.util.context import Context


def verbose(context: Context, value: Any) -> None:
    context.verbose = value