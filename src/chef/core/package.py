import json
import platform
from dataclasses import dataclass

from pathlib import Path
from typing import Any


@dataclass
class PackageScript:
    build: Path | None
    verify: Path | None


@dataclass
class Package:
    name: str
    description: str
    version: str
    url: str
    sha256: str
    script: PackageScript


def extract(path: Path) -> Package:
    """Extracts a Chef package into a Package object"""
    data: Any

    with open(str(path), "r") as f:
        data = json.load(f)

    package = Package(
        name=data["name"],
        description=data["description"],
        version=data["version"],
        url="",  # will be replaced
        sha256="",  # will be replaced
        script=PackageScript(build=None, verify=None),
    )

    # This ensures the code follow the registry's specification,
    # allowing the usage of Linux or macOS specific download URLs.
    if data["linux"] or data["macOS"]:
        os = "linux" if platform.system() == "Linux" else "macOS"

        package.url = data[os]["url"].format(version=data["version"])
        package.sha256 = data[os]["sha256"]
    else:
        package.url = data["url"]
        package.sha256 = data["sha256"]

    if (build_script_path := path.parent / "build.sh").exists():
        package.script.build = build_script_path

    if (verify_script_path := path.parent / "verify.sh").exists():
        package.script.verify = verify_script_path

    return package
