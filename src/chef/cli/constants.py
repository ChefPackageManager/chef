from chef.cli.command import (
    verbose,
    version,
    install,
    upgrade,
    audit
)
from chef.cli.util import Argument, ArgumentKey

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
    ArgumentKey.AUDIT: Argument(
        long_name="--audit",
        shorthand="-A",
        switch=True,
        handler=audit
    )
}
