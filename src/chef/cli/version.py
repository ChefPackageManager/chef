from typing import Any

from chef import __version__
from chef.cli.util.context import Context


def version(context: Context, value: Any) -> None:
    print(__version__)