import argparse
import enum
from dataclasses import dataclass
from typing import Callable, Any

from chef.core.chef import Chef


class Context:
    """
    A context reflecting the state of the app to the CLI, shared between the individual CLI functions and `main`.
    """

    verbose: bool
    chef: Chef
    crash: Callable[[], None]

    def __init__(self, on_crash: Callable[[], None], chef: Chef):
        self.crash = on_crash
        self.chef = chef


class ArgumentKey(enum.Enum):
    VERBOSE = enum.auto()
    VERSION = enum.auto()
    INSTALL = enum.auto()
    UPGRADE = enum.auto()
    REMOVE = enum.auto()
    PACKAGES = enum.auto()


@dataclass
class Argument:
    long_name: str
    shorthand: str
    handler: Callable[[Context, Any], None]
    switch: bool = False


def parse_args(
    prog: str, description: str, recognised: dict[ArgumentKey, Argument]
) -> dict[ArgumentKey, Any]:
    """Parses `argv` on the basis of the `args` parameter accepted on this function."""
    parser = argparse.ArgumentParser(prog=prog, description=description)

    # we need to add the arguments defined to be parsed to the parser
    # in a way that `argparse` it understands.
    for key, value in recognised.items():
        parser.add_argument(
            value.long_name,
            value.shorthand,
            action="store_true" if value.switch else None,
        )

    parsed = parser.parse_args()
    rv = {}

    # this part *extracts* the parsed values and converts it into a
    # much nicer format which can be retrieved via an `ArgumentKey`.
    for key, arg in recognised.items():
        long_name = arg.long_name[2:]  # remove the "--" prefix
        parsed_value = getattr(parsed, long_name)

        # indicates that no value likely was provided, or the user provided a negative flag.
        if parsed_value is None or not parsed_value:
            continue

        rv[key] = parsed_value

    return rv


def delegate(
    all_args: dict[ArgumentKey, Argument],
    context: Context,
    provided_args: dict[ArgumentKey, Any],
) -> None:
    """Delegates the provided CLI arguments to their respective handlers."""
    for key, value in provided_args.items():
        all_args[key].handler(context, value)
