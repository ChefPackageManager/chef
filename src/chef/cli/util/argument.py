import dataclasses
import enum
from typing import Callable, Any

from chef.cli import Context


class ArgumentKey(enum.Enum):
    VERBOSE = enum.auto()
    VERSION = enum.auto()
    INSTALL = enum.auto()
    UPGRADE = enum.auto()
    AUDIT = enum.auto()


@dataclasses.dataclass
class Argument:
    long_name: str
    shorthand: str
    handler: Callable[[Context, Any], None]
    switch: bool = False
