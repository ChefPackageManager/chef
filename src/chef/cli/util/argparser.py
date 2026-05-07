import argparse
from typing import Any

from chef.cli import ARGUMENTS
from chef.cli.util.argument import ArgumentKey

class ArgParser:
    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="chef",
            description="Security-focused utility for installing software for macOS & Linux."
        )

    def construct(self) -> None:
        for key, argument in ARGUMENTS.items():
            self.parser.add_argument(
                argument.long_name,
                argument.shorthand,
                action="store_true" if argument.switch else None
            )

    def parse(self) -> dict[ArgumentKey, Any]:
        parsed_arguments_as_namespace = self.parser.parse_args()

        rv = {}

        for key, argument in ARGUMENTS.items():
            parsed_value = getattr(
                parsed_arguments_as_namespace,
                argument.long_name[2:]
            )

            # indicates that no value likely was provided, or the user provided a negative flag.
            if parsed_value is None or not parsed_value:
                continue


            rv[key] = parsed_value

        return rv
