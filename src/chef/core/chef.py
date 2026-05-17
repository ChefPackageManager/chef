import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List

import requests

from chef.core.package import Package
from chef.core.registry import Registry
from chef.util import file, checksum


class PackageAlreadyInstalledError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} is already installed!")


class PackageNotInstalledError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} is not installed!")


class PackageIntegrityVerificationFailedError(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package: {package_name} failed verification and may've be tampered with!")


@dataclass
class ChefPath:
    prefix: Path
    bin: Path
    registries: Path
    tmp: Path


class Chef:
    """ Handles the core functionality of the package manager, such as installing, building, updating, etc """

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
        """ Initialises the required directories needed by Chef """
        if not self.path.prefix.exists():
            self.path.prefix.mkdir()

        if not self.path.bin.exists():
            self.path.bin.mkdir()

        if not self.path.registries.exists():
            self.path.registries.mkdir()

        if self.path.tmp.exists():
            shutil.rmtree(self.path.tmp)

        self.path.tmp.mkdir()

        if not self.registry.path.exists():
            self.registry.download()

    def installed(self, package: Package) -> bool:
        """ Checks if a given package is installed or not """
        return (self.path.bin / package.name).exists()

    def build(self, package: Package, cwd: Path) -> None:
        """ Builds a given package from source in the context of the directory given """
        env = os.environ.copy()
        env["CHEF_HOME"] = str(self.path.prefix)
        env["PACKAGE_NAME"] = package.name
        env["OS"] = "MACOS" if platform.system() == "Darwin" else "LINUX"

        subprocess.run(
            ["/usr/bin/env", "sh", str(package.script.build)],
            cwd=cwd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def install(self, package: Package) -> None:
        """ This is the entrypoint for the installation of a new package. """
        if self.installed(package):
            raise PackageAlreadyInstalledError(package.name)

        r = requests.get(package.url)

        try:
            r.raise_for_status()
        except Exception as e:
            raise e

        filename = package.url.split("/")[-1]

        with open(str(self.path.tmp / filename), "wb") as f:
            f.write(r.content)

        if not checksum.verify(self.path.tmp / filename, against=package.sha256):
            raise PackageIntegrityVerificationFailedError

        extracted_at = file.unpack(self.path.tmp / filename)

        (self.path.bin / package.name).mkdir()

        self.build(package, cwd=extracted_at)

    def upgrade(self) -> None:
        """ Upgrades packages, but currently only synchronises with the remote registry """
        self.registry.update()

    def remove(self, package: Package) -> None:
        """ Removes an installed package """
        if not self.installed(package):
            raise PackageNotInstalledError(package.name)

        shutil.rmtree(
            self.path.bin / package.name
        )

    def find_package(self, package_name: str) -> Package | None:
        """ Finds a package by its package name """
        filtered = [package for package in self.registry.packages() if package.name == package_name]

        if len(filtered) == 0:
            return None

        return filtered[0]

    def packages(self) -> List[Package]:
        """ Lists all packages in Chef's associated registry """
        return self.registry.packages()
