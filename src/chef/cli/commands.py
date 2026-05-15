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

    try:
        context.chef.install()
    except:
        pass

    log.info(f"Installing: {maybe_package_name}...")


def upgrade(context: Context, value: Any) -> None:
    spinner = log.spinner()

    context.chef.upgrade()
    spinner.stop()


def audit(context: Context, value: Any) -> None:
    spinner = log.spinner()

    context.chef.audit()
    spinner.stop()


def verbose(context: Context, value: Any) -> None:
    context.verbose = value

def packages(context: Context, value: Any) -> None:
    print("Packages:")

    for package in context.chef.packages():
        print(f"  * {package.name} [v{package.version}]")

def version(context: Context, value: Any) -> None:
    print(__version__)
