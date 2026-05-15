import subprocess
import requests
from pathlib import Path
from typing import List

from requests import HTTPError

from chef.core.package import Package
from chef.core.registry import Registry

class PackageAlreadyInstalledError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} is already installed")

class Chef:
    registry: Registry
    prefix: Path

    def __init__(self, prefix: Path, registry_url: str):
        self.installed_packages = []
        self.prefix = prefix

        self.registry = Registry(
            registry_url,
            prefix / "registries" / "registry"
        )

    def bootstrap(self) -> None:
        if not self.prefix.exists():
            self.prefix.mkdir()

        if not (bin_dir := self.prefix / "bin").exists():
            bin_dir.mkdir()

        if not (registries_dir := self.prefix / "registries").exists():
            registries_dir.mkdir()

        if not (tmp_dir := self.prefix / "tmp").exists():
            tmp_dir.mkdir()

        if not self.registry.path.exists():
            self.registry.download()

    def installed(self, package: Package) -> bool:
        return (self.prefix / "bin" / package.name).exists()

    def install(self, package: Package) -> None:
        if self.installed(package):
            raise PackageAlreadyInstalledError(package.name)

        package_path = self.prefix / "bin" / package.name
        package_path.mkdir()

        r = requests.get(package.url)

        try:
            r.raise_for_status()
        except Exception as e:
            package_path.rmdir()
            raise e



    def upgrade(self) -> None:
        self.registry.update()

    def audit(self) -> None:
        pass

    def packages(self) -> List[Package]:
        return self.registry.packages()
