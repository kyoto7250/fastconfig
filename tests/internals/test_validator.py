import sys
import unittest
from dataclasses import MISSING, Field
from typing import Any, Optional

from fastconfig import MissingRequiredElementError, UnexpectedValueError
from fastconfig.internals.validator import DEFAULT_VALUE, _extract, _Validator


class Test_extract(unittest.TestCase):
    def test___extract(self) -> None:
        dic: dict[str, Any] = {
            "value": 1,
            "internal": {"value": 2, "internal": {"value": 3}},
        }

        self.assertEqual(_extract(dic, "value"), 1)
        self.assertIsNone(_extract(dic, "val"))
        self.assertEqual(_extract(dic, ["value"]), 1)
        self.assertIsNone(_extract(dic, ["val"]))
        self.assertEqual(
            _extract(dic, ["internal"]), {"value": 2, "internal": {"value": 3}}
        )
        self.assertEqual(_extract(dic, ["internal", "value"]), 2)
        self.assertIsNone(_extract(dic, ["internal", "val"]))
        self.assertEqual(_extract(dic, ["internal", "internal", "value"]), 3)
        self.assertIsNone(_extract(dic, ["internal", "internal", "val"]))


class FieldBuilder:
    @classmethod
    def build(
        cls, default: Any, ty: type, metadata: Optional[dict[str, Any]] = None
    ) -> Field:
        dic = cls.kwargs()
        dic["default"] = default
        dic["metadata"] = metadata
        f = Field(**dic)
        f.type = ty
        return f

    @classmethod
    def kwargs(cls) -> dict[str, Any]:
        options: dict[str, Any] = {
            "default": MISSING,
            "default_factory": MISSING,
            "init": True,
            "repr": True,
            "hash": None,
            "compare": True,
            "metadata": None,
        }

        if sys.version_info >= (3, 10):
            options["kw_only"] = MISSING
        return options


class TestValidator(unittest.TestCase):
    def test_call(self) -> None:
        setting = {"int": 42, "not_int": "42"}
        validator = _Validator(setting)

        self.assertEqual(
            validator(
                "int",
                FieldBuilder.build(default=0, ty=int, metadata={"key": "int"}),
            ),
            42,
        )

        self.assertIsInstance(
            validator(
                "int",
                FieldBuilder.build(default=0, ty=int, metadata={"key": "not exist"}),
            ),
            DEFAULT_VALUE,
        )

        # no default
        with self.assertRaises(MissingRequiredElementError) as me:
            validator(
                "int",
                FieldBuilder.build(
                    default=MISSING, ty=int, metadata={"key": "not exist"}
                ),
            )
        self.assertEqual(
            str(me.exception),
            "key: int is not found",
        )

        with self.assertRaises(UnexpectedValueError) as ue:
            validator(
                "int",
                FieldBuilder.build(default=0, ty=int, metadata={"key": "not_int"}),
            )

        self.assertEqual(
            str(ue.exception),
            "int: 42 is not valid type. must be of type <class 'int'>",
        )
