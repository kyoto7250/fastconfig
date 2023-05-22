import unittest

from fastconfig import InvalidConfigError
from fastconfig.internals.loader import _FileLoader


class TestLoader(unittest.TestCase):
    def test_call(self) -> None:
        loader = _FileLoader()
        with self.assertRaises(InvalidConfigError) as je:
            loader("tests/fixtures/internals/invalid.json")

        self.assertEqual(str(je.exception), "Expecting value: line 1 column 1 (char 0)")

        with self.assertRaises(InvalidConfigError):
            loader("tests/fixtures/internals/invalid.toml")

        with self.assertRaises(InvalidConfigError) as ue:
            loader("tests/fixtures/internals/unsupported.txt")
        self.assertEqual(
            str(ue.exception), "FastConfig only supports json and toml formats now"
        )

        self.assertEqual(
            loader("tests/fixtures/internals/non_dict.json"), {"content": [1, 2, 3]}
        )
