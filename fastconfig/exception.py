class FastConfigError(Exception):
    ...


class ValidationError(FastConfigError):
    ...


class InvalidConfigError(FastConfigError):
    ...


class MissingRequiredElementError(FastConfigError):
    ...


class UnexpectedValueError(FastConfigError):
    ...
