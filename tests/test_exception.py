import unittest

from fastconfig.exception import (
    FastConfigError,
    InvalidConfigError,
    MissingRequiredElementError,
    UnexpectedValueError,
)


class TestFastConfigError(unittest.TestCase):
    def test_error(self) -> None:
        with self.assertRaises(FastConfigError):
            raise InvalidConfigError

        with self.assertRaises(FastConfigError):
            raise UnexpectedValueError

        with self.assertRaises(FastConfigError):
            raise MissingRequiredElementError()
