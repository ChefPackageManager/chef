from typing import Any

from chef import __version__
from chef.cli.util import Context
from chef.util import log


def install(context: Context, maybe_package_name: Any) -> None:
    package_name = maybe_package_name

    try:
        assert type(package_name) is str
    except TypeError:
        log.error("Invalid package name to install provided!")
        context.crash()


def upgrade(context: Context, value: Any) -> None:
    print("Upgrade")


def audit(context: Context, value: Any) -> None:
    print("Audit")


def verbose(context: Context, value: Any) -> None:
    context.verbose = value
    log.info("Verbose mode is enabled")


def version(context: Context, value: Any) -> None:
    print(__version__)
