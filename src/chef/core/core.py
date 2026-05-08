from typing import List
from dataclasses import dataclass

from chef.core.package import Package

@dataclass
class ActionResult:
    message: str
    error: bool


class Chef:
    installed_packages: List[Package]

    def install(self, package: Package) -> ActionResult:
        pass

    def upgrade(self) -> ActionResult:
        pass

    def audit(self) -> ActionResult:
        pass
