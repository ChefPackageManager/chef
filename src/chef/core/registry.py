from pathlib import Path
from typing import List

from chef.core.package import Package, extract
from chef.util import git


class PackageNotInRegistryError(Exception):
    def __init__(self):
        super().__init__("Package is not available in the registry!")


class Registry:
    """ A registry in Chef is a repository holding packages with associated JSON & scripts """
    url: str
    path: Path

    def __init__(self, url: str, path: Path):
        self.url = url
        self.path = path

    def download(self) -> None:
        """ Downloads the registry, with the class instance's URL and Path, onto the user's device """
        git.clone(self.path.parent, self.url)

    def update(self) -> None:
        """ Pulls the latest version of the registry """
        git.pull(self.path)

    def packages(self) -> List[Package]:
        """ Lists all packages in this registry """
        manifests = [manifest for manifest in (self.path / "packages").glob("*/*.json")]

        packages = []
        for manifest in manifests:
            package = extract(manifest)
            packages.append(package)

        return packages

    def has(self, package: Package) -> bool:
        """ Checks if a given package is available from this registry """
        return package.name in self.packages()
