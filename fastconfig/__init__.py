"""This package provides the methods to search files."""
import os
from pathlib import Path
from typing import List, Optional, Union

__version__ = "0.2.0"
PROJECT_ROOTS: List[str] = [".hg", ".git"]
DEPTH: int = 10


def is_project_root(path: Union[str, Path]) -> bool:
    """
    Check the given path is the project root directory or not.

    This method determines the project root by whether the version control tool directory exists.

    Args:
        path (Union[str, Path]):
            The path to check whether it is the project root or not

    Returns:
        bool: The result of the project root or not
    """
    if isinstance(path, str):
        path = Path(path)

    if path.is_file():
        path = path.parent

    for candidate in PROJECT_ROOTS:
        if path.joinpath(candidate).is_dir():
            return True
    return False


def find_project_root(path: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """
    Return if the project root is found, or None if not.

    Args:
        path (Optional[Union[str, Path]]):
            A path string or Path object to start searching, If nothing is passed, start in the current directory

    Returns:
        Optional[Path]: the project root path, or None if the project root is not found
    """
    if path is None:
        path = os.getcwd()
    cnt: int = 0

    candidate: Path = Path(path) if isinstance(path, str) else path
    if is_project_root(candidate):
        return candidate

    while cnt < DEPTH:
        candidate = candidate.parent
        if is_project_root(candidate):
            return candidate

        if candidate.parent == candidate:
            return None

        cnt += 1
    return None


def search(
    target: Union[str, Path],
    path: Optional[Union[str, Path]] = None,
    end_up_the_project_root: bool = True,
) -> Optional[Path]:
    """
    Recursively searches for files with the name of the target and returns the result.

    Args:
        target (Union[str, Path]):
            Search target filename, and directory names are ignored.

        path (Optional[Union[str, Path]]):
            A path string or Path object to start searching, If nothing is passed, start in the current directory.

        end_up_the_project_root (bool):
            Whether or not to search the directory where the version control tool exists

    Returns:
        Optional[Path]: a path of the target file, or None if the target file is not found
    """
    if isinstance(target, str):
        target = Path(target)

    target_name: str = target.name
    if path is None:
        path = os.getcwd()

    cnt: int = 0
    candidate: Path = Path(os.path.join(path, target_name))
    if candidate.exists():
        return candidate
    if is_project_root(candidate):
        return None

    while cnt < DEPTH:
        candidate = candidate.parent.parent.joinpath(target_name)
        if candidate.exists():
            return candidate

        if candidate.parent.parent.joinpath(target_name) == candidate or (
            end_up_the_project_root and is_project_root(candidate)
        ):
            return None

        cnt += 1
    return None
