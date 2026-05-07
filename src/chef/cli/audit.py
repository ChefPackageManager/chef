from typing import Any

from chef.cli.util.context import Context


def audit(context: Context, value: Any) -> None:
    print("Audit")