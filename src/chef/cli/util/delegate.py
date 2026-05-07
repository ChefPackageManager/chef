from typing import Any

from .context import Context
from .. import ARGUMENTS, ArgumentKey


def delegate(context: Context, args: dict[ArgumentKey, Any]) -> None:
    for key, value in args.items():
        ARGUMENTS[key].handler(context, value)