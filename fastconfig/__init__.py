"""This package provides public modules."""


from fastconfig.config import FastConfig, fc_field
from fastconfig.exception import (
    FastConfigError,
    InvalidConfigError,
    MissingRequiredElementError,
    UnexpectedValueError,
)
from fastconfig.searcher import find_project_root, is_project_root, search
from fastconfig.version import VERSION

__version__ = VERSION
__all__ = [
    "fc_field",
    "FastConfig",
    "FastConfigError",
    "InvalidConfigError",
    "MissingRequiredElementError",
    "UnexpectedValueError",
    "find_project_root",
    "is_project_root",
    "search",
]
