import tarfile
from pathlib import Path


class UnpackError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def _zip(path: Path) -> Path:
    pass


def _tgz(path: Path) -> Path:
    with tarfile.open(str(path), "r:gz") as tar:
        extracted_dirname = tar.getnames()[0]
        tar.extractall(path=path.parent, filter="data")

    return path.parent / extracted_dirname


def extension(path: Path) -> str:
    filename = str(path).split("/")[-1]

    filename_extension = filename.rsplit(".", 1)[-1]

    # if the extension is ".gz" or ."xz", just check it to see if
    # the previous substring is "tar", and in such a case, utilise it.

    if filename_extension in ("gz", "xz") and (long_ext := filename.rsplit(".", 2)[-2:]) == "tar":
        filename_extension = long_ext

    return filename_extension


def unpack(path: Path) -> Path:
    rv: Path = Path()  # I initialise this variable just to appease PyCharm's linter

    match extension(path):
        case "tar.gz":
            rv = _tgz(path)
        case "tgz":
            rv = _tgz(path)
        case "zip":
            rv = _zip(path)
        case _:
            raise UnpackError(f"Cannot unpack the provided file extension: {extension(path)}")

    return rv
