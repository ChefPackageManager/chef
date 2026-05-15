import sys
from pathlib import Path

from chef.cli.constants import RECOGNISED_ARGUMENTS
from chef.cli.util import Context, delegate, parse_args
from chef.core.chef import Chef
from chef.util import log
from chef.util.git import GitNotInstalledError, GitCloneError

CHEF_HOME = Path.home() / ".chef-package-manager"
REPO_URL = "https://github.com/ChefPackageManager/registry.git"

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
    except GitCloneError as e:
        log.error(f"Something went wrong while cloning:\n{e}")

    context = Context(crash, chef)
    delegate(RECOGNISED_ARGUMENTS, context, parsed)
