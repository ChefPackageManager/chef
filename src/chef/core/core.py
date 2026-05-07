from typing import List

from . import Result
from .package import Package


class Chef:
    installed_packages: List[Package]

    def install(self, package: Package) -> Result:
        pass

    def upgrade(self) -> Result:
        pass

    def audit(self) -> Result:
        pass