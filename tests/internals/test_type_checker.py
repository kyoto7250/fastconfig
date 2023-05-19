import unittest
from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Any, Callable, Optional, Union

from fastconfig.exception import UnexpectedValueError
from fastconfig.internals.type_checker import _TypeChecker

Numeric = Union[int, float]


@dataclass
class ComplexTypes:
    a: Union[int, float] = 0
    b: Union[str, Union[int, float]] = 0
    c: Optional[int] = field(default=None)
    d: dict[str, dict[str, int]] = field(default_factory=dict)
    e: Any = 0
    f: Numeric = field(default=0)


class TestTypeChecker(unittest.TestCase):
    def test_call(self) -> None:
        checker = _TypeChecker()
        config = ComplexTypes()
        for key, f in config.__dataclass_fields__.items():
            self.assertEqual(
                checker(key, getattr(config, key), f.type),
                getattr(config, key),
            )

        with self.assertRaises(UnexpectedValueError) as e:
            checker("key", "10", int)

        self.assertEqual(
            str(e.exception), "key: 10 is not valid type. must be of type <class 'int'>"
        )

    def test_check(self) -> None:
        checker = _TypeChecker()

        # Any
        self.assertTrue(checker.check("Any", 10, Any))  # type: ignore

        # Union
        self.assertTrue(checker.check("Union[int, float]", 10, Union[int, float]))  # type: ignore
        self.assertTrue(checker.check("Union[int, str]", "10", Union[int, str]))  # type: ignore
        self.assertTrue(checker.check("Union[int, Any]", "10", Union[int, Any]))  # type: ignore
        self.assertFalse(checker.check("Union[int, float]", "10", Union[int, float]))  # type: ignore

        # list
        self.assertTrue(checker.check("List[int]", [1, 2, 3], list[int]))
        self.assertFalse(checker.check("List[str]", [1, 2, 3], list[str]))
        self.assertTrue(checker.check("List[str]", ["1"], list[str]))
        self.assertTrue(checker.check("List[str]", [], list[str]))
        self.assertFalse(checker.check("not list", {1: 1}, list[int]))

        # dict
        self.assertTrue(checker.check("dict[int, int]", {1: 1}, dict[int, int]))
        self.assertTrue(checker.check("dict[int, str]", {1: "1"}, dict[int, str]))
        self.assertFalse(checker.check("dict[int, str]", {"1": "1"}, dict[int, str]))
        self.assertFalse(checker.check("dict[int, str]", {1: 1}, dict[int, str]))
        self.assertTrue(
            checker.check(
                "dict[int, dict[int, str]]", {1: {1: "1"}}, dict[int, dict[int, str]]
            )
        )
        self.assertFalse(
            checker.check(
                "dict[int, dict[int, str]]", {"1": {1: 1}}, dict[int, dict[int, str]]
            )
        )
        self.assertFalse(checker.check("not dict", [1, 2], dict[int, int]))

        # Optional
        self.assertTrue(checker.check("Optional[int]", 1, Optional[int]))  # type: ignore
        self.assertTrue(checker.check("Optional[int]", None, Optional[int]))  # type: ignore
        self.assertFalse(checker.check("Optional[int]", "str", Optional[int]))  # type: ignore
        self.assertTrue(
            checker.check("Optional[dict[int, int]]", {1: 1}, Optional[dict[int, int]])  # type: ignore
        )
        self.assertFalse(
            checker.check(
                "Optional[dict[int, int]]", {1: "1"}, Optional[dict[int, int]]  # type: ignore
            )
        )

        # other type
        with self.assertRaises(UnexpectedValueError) as e:
            checker.check("lambda", lambda f: f * 2, Callable[[int], int])  # type: ignore

        self.assertEqual(
            str(e.exception), "typing.Callable[[int], int] is not supported"
        )

    def test_check_datetime(self) -> None:
        checker = _TypeChecker()

        # original
        self.assertTrue(checker.check_datetime(datetime(2020, 1, 1), datetime))
        self.assertTrue(checker.check_datetime(time(0, 0, 0), time))
        self.assertTrue(checker.check_datetime(date(2020, 1, 1), date))

        # convert
        self.assertTrue(checker.check_datetime(datetime(2020, 1, 1), date))
        self.assertTrue(checker.check_datetime(datetime(2020, 1, 1), time))

        # cannot convert
        self.assertFalse(checker.check_datetime(time(0, 0, 0), date))
        self.assertFalse(checker.check_datetime(date(2020, 1, 1), datetime))

        # str to date / datetime
        self.assertFalse(checker.check_datetime("apple", date))
        self.assertTrue(checker.check_datetime("2020-10-01", date))
        self.assertFalse(checker.check_datetime("2020-10-01", time))
        self.assertTrue(checker.check_datetime("2020-10-01", datetime))
