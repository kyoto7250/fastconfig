"""this module provides Exceptions in FastConfig."""


class FastConfigError(Exception):
    """super class for all errors returned by FastConfig."""

    ...


class InvalidConfigError(FastConfigError):
    """exception when providing files or classes in unsupported formats."""

    ...


class MissingRequiredElementError(FastConfigError):
    """exception when providing `field` has no default value and the corresponding value could not be read from the file."""

    ...


class UnexpectedValueError(FastConfigError):
    """exception whe providing failed type-checking."""

    ...
