import dataclasses
import pathlib

from chef.core import Result


@dataclasses.dataclass
class Package:
    name: str
    url: str
    sha256: str
    signer: str
    path: pathlib.Path

    def download(self, download_path: pathlib.Path) -> Result:
        raise NotImplementedError

    def install(self) -> Result:
        raise NotImplementedError

    def upgrade(self) -> Result:
        raise NotImplementedError

    def verify(self) -> Result:
        raise NotImplementedError
