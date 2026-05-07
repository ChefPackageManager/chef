import sys

from chef.cli.util import argparser
from chef.cli.util.delegate import delegate
from chef.cli.util.context import Context

def crash() -> None:
    sys.exit(1)

def main() -> None:
    parser = argparser.ArgParser()
    parser.construct()

    args = parser.parse()

    context = Context(crash)
    delegate(context, args)
