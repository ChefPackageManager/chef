import os
import shutil
import subprocess
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import List

import requests

from chef.core.package import Package
from chef.core.registry import Registry
from chef.util import file


class PackageAlreadyInstalledError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} is already installed!")


class PackageNotInstalledError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} is not installed!")


def verify(archive: Path, package: Package) -> bool:
    hasher = sha256()

    with open(archive, "rb") as f:
        hasher.update(
            f.read()
        )

    return hasher.hexdigest() == package.sha256


@dataclass
class ChefPath:
    prefix: Path
    bin: Path
    registries: Path
    tmp: Path


class Chef:
    registry: Registry
    path: ChefPath

    def __init__(self, prefix: Path, registry_url: str):
        self.path = ChefPath(
            prefix,
            bin=prefix / "bin",
            registries=prefix / "registries",
            tmp=prefix / "tmp"
        )

        self.registry = Registry(
            registry_url,
            self.path.registries / "registry"
        )

    def bootstrap(self) -> None:
        if not self.path.prefix.exists():
            self.path.prefix.mkdir()

        if not self.path.bin.exists():
            self.path.bin.mkdir()

        if not self.path.registries.exists():
            self.path.registries.mkdir()

        shutil.rmtree(self.path.tmp)
        self.path.tmp.mkdir()

        if not self.registry.path.exists():
            self.registry.download()

    def installed(self, package: Package) -> bool:
        return (self.path.bin / package.name).exists()

    def build(self, cwd: Path, package: Package) -> None:
        env = os.environ.copy()
        env["CHEF_HOME"] = str(self.path.prefix)
        env["PACKAGE_NAME"] = package.name

        subprocess.run(
            ["/usr/bin/env", "sh", str(package.script.build)],
            cwd=cwd,
            env=env
        )

    def install(self, package: Package) -> None:
        if self.installed(package):
            raise PackageAlreadyInstalledError(package.name)

        package_path = self.path.bin / package.name
        package_path.mkdir()

        r = requests.get(package.url)

        try:
            r.raise_for_status()
        except Exception as e:
            package_path.rmdir()
            raise e

        filename = package.url.split("/")[-1]

        with open(str(self.path.tmp / filename), "wb") as f:
            f.write(r.content)

        if not verify(self.path.tmp / filename, package):
            raise ValueError("Failed to verify that the downloaded file wasn't tampered with or corrupted!")

        extracted_at = file.unpack(self.path.tmp / filename)

        self.build(cwd=extracted_at, package=package)

    def upgrade(self) -> None:
        self.registry.update()

    def remove(self, package: Package) -> None:
        if not self.installed(package):
            raise PackageNotInstalledError(package.name)

        shutil.rmtree(
            self.path.bin / package.name
        )

    def find_package(self, package_name: str) -> Package | None:
        filtered = [package for package in self.registry.packages() if package.name == package_name]

        if len(filtered) == 0:
            return None

        return filtered[0]

    def packages(self) -> List[Package]:
        return self.registry.packages()
