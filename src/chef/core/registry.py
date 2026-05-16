from pathlib import Path
from typing import List

from chef.core.package import Package, extract
from chef.util import git


class PackageNotInRegistryError(Exception):
    def __init__(self):
        super().__init__("Package is not available in the registry!")


class Registry:
    url: str
    path: Path

    def __init__(self, url: str, path: Path):
        self.url = url
        self.path = path

    def download(self) -> None:
        git.clone(self.path.parent, self.url)

    def update(self) -> None:
        git.pull(self.path)

    def packages(self) -> List[Package]:
        manifests = [manifest for manifest in (self.path / "packages").glob("*/*.json")]

        packages = []
        for manifest in manifests:
            package = extract(manifest)
            packages.append(package)

        return packages

    def has(self, package: Package) -> bool:
        return package.name in self.packages()
