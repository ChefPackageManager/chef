from typing import Any

from chef import __version__
from chef.cli.util import Context
from chef.core.registry import PackageNotInRegistryError
from chef.util import log


def install(context: Context, package_name: str) -> None:
    try:
        package = context.chef.find_package(package_name)

        if package is None:
            raise PackageNotInRegistryError

        context.chef.install(package)
    except Exception as e:
        log.error(str(e))


def upgrade(context: Context, value: Any) -> None:
    spinner = log.spinner()

    context.chef.upgrade()
    spinner.stop()


def remove(context: Context, package_name: str) -> None:
    try:
        package = context.chef.find_package(package_name)

        if package is None:
            raise PackageNotInRegistryError

        context.chef.remove(package)
    except Exception as e:
        log.error(str(e))


def verbose(context: Context, value: Any) -> None:
    context.verbose = value


def packages(context: Context, value: Any) -> None:
    print("Packages:")

    for package in context.chef.packages():
        installed_message = " (INSTALLED)" if context.chef.installed(package) else ""
        print(f"  * {package.name} [v{package.version}]{installed_message}")


def version(context: Context, value: Any) -> None:
    print(__version__)
