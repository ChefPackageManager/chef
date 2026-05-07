from typing import Any

from chef.cli.util.context import Context
from chef.core.package import Package
from chef.util import log


def install(context: Context, maybe_package_name: Any) -> None:
    package_name = maybe_package_name

    try:
        assert type(package_name) is str
    except TypeError:
        log.error("Invalid package name to install provided!")
        context.crash()

    package = Package()