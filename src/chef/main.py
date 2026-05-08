import sys

from chef.cli.constants import RECOGNISED_ARGUMENTS
from chef.cli.util import Context, delegate, parse_args


def crash() -> None:
    sys.exit(1)


def main() -> None:
    parsed = parse_args(
        prog="chef",
        description="Security-focused utility for installing software for macOS & Linux.",
        recognised=RECOGNISED_ARGUMENTS
    )

    context = Context(crash)
    delegate(RECOGNISED_ARGUMENTS, context, parsed)
