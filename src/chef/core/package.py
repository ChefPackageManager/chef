import pathlib
from dataclasses import dataclass

from chef.core.core import ActionResult


@dataclass
class Package:
    name: str
    url: str
    sha256: str
    signer: str
    path: pathlib.Path

    def download(self, download_path: pathlib.Path) -> ActionResult:
        raise NotImplementedError

    def install(self) -> ActionResult:
        raise NotImplementedError

    def upgrade(self) -> ActionResult:
        raise NotImplementedError

    def verify(self) -> ActionResult:
        raise NotImplementedError
