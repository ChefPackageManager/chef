from hashlib import sha256
from pathlib import Path


def verify(file: Path, *, against: str) -> bool:
    hasher = sha256()

    with open(file, "rb") as f:
        hasher.update(f.read())

    return hasher.hexdigest() == against
