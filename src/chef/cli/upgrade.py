from typing import Any

from chef.cli.util.context import Context


def upgrade(context: Context, value: Any) -> None:
    print("Upgrade")