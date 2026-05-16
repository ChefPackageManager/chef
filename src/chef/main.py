import sys
from pathlib import Path

from chef.cli.commands import (
    verbose,
    version,
    install,
    upgrade,
    remove,
    packages
)
from chef.cli.util import Context, delegate, parse_args, ArgumentKey, Argument
from chef.core.chef import Chef
from chef.util import log
from chef.util.git import GitNotInstalledError, GitCloneError

CHEF_HOME = Path.home() / ".chef-package-manager"
REPO_URL = "https://github.com/ChefPackageManager/registry.git"

RECOGNISED_ARGUMENTS = {
    ArgumentKey.VERBOSE: Argument(
        long_name="--verbose",
        shorthand="-v",
        switch=True,
        handler=verbose
    ),
    ArgumentKey.VERSION: Argument(
        long_name="--version",
        shorthand="-V",
        switch=True,
        handler=version
    ),
    ArgumentKey.INSTALL: Argument(
        long_name="--install",
        shorthand="-i",
        handler=install
    ),
    ArgumentKey.UPGRADE: Argument(
        long_name="--upgrade",
        shorthand="-U",
        switch=True,
        handler=upgrade
    ),
    ArgumentKey.REMOVE: Argument(
        long_name="--remove",
        shorthand="-R",
        handler=remove
    ),
    ArgumentKey.PACKAGES: Argument(
        long_name="--packages",
        shorthand="-P",
        switch=True,
        handler=packages
    )
}


def crash() -> None:
    sys.exit(1)


def main() -> None:
    parsed = parse_args(
        prog="chef",
        description="Security-focused utility for installing software for macOS & Linux.",
        recognised=RECOGNISED_ARGUMENTS
    )

    chef = Chef(CHEF_HOME, REPO_URL)

    try:
        chef.bootstrap()
    except GitNotInstalledError:
        log.error("You need to have `git` installed on your system to continue!")
    except GitCloneError:
        log.error(f"Something went wrong while cloning!")

    context = Context(crash, chef)
    delegate(RECOGNISED_ARGUMENTS, context, parsed)
