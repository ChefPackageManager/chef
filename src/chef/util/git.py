import shutil
import subprocess
from pathlib import Path


class GitError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class GitCloneError(GitError):
    def __init__(self, reason: str):
        super().__init__(f"Failed to clone: {reason}")


class GitPullError(GitError):
    def __init__(self):
        super().__init__("Failed to perform `git pull`, please check your connection!")


class GitNotInstalledError(GitError):
    def __init__(self):
        super().__init__("Git is not installed!")


def _is_git_installed() -> bool:
    return shutil.which("git") is not None


def _git_executable() -> str:
    path = shutil.which("git")

    if path is None:
        raise GitNotInstalledError

    return path


def clone(path: Path, url: str) -> None:
    if not _is_git_installed():
        raise GitNotInstalledError

    result = subprocess.run(
        args=[_git_executable(), "clone", url], cwd=str(path), capture_output=True
    )

    if result.returncode != 0:
        raise GitCloneError(str(result.stderr))


def pull(at: Path) -> None:
    if not _is_git_installed():
        raise GitNotInstalledError

    result = subprocess.run(
        args=[_git_executable(), "pull"], cwd=str(at), capture_output=True
    )

    if result.returncode != 0:
        raise GitPullError
