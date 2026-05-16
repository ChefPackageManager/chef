import json
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
    """ Extracts a Chef package into a Package object """
    data: Any

    with open(str(path), "r") as f:
        data = json.load(f)

    package = Package(
        name=data["name"],
        description=data["description"],
        version=data["version"],
        url=data["url"].format(version=data["version"]),
        sha256=data["sha256"],
        script=PackageScript(
            build=None,
            verify=None
        )
    )

    if (build_script_path := path.parent / "build.sh").exists():
        package.script.build = build_script_path

    if (verify_script_path := path.parent / "verify.sh").exists():
        package.script.verify = verify_script_path

    return package
