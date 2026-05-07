from typing import Any, Callable

from chef.cli.audit import audit
from chef.cli.install import install
from chef.cli.upgrade import upgrade
from chef.cli.verbose import verbose
from chef.cli.version import version

from chef.cli.util.context import Context
from chef.cli.util.argument import Argument, ArgumentKey

ARGUMENTS = {
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
    ArgumentKey.AUDIT: Argument(
        long_name="--audit",
        shorthand="-A",
        switch=True,
        handler=audit
    )
}
