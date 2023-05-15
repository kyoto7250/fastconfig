import unittest
from dataclasses import dataclass, field
from datetime import date
from typing import Any, List, Optional, Union

from fastconfig.config import ConfigBuilder, FastConfig, Metadata
from fastconfig.exception import InvalidConfigError


@dataclass
class BasicTypes(FastConfig):
    a: dict[str, str] = field(
        default_factory=dict, metadata=Metadata({"section": ["table"]})
    )
    b: bool = field(default=False, metadata=Metadata({"section": ["flag"]}))
    c: int = field(default=0, metadata=Metadata({"section": ["section", "int"]}))
    d: str = field(default="default", metadata=Metadata({"section": "str"}))
    e: List[int] = field(
        default_factory=list,
        metadata=Metadata({"section": ["section", "list", "value"]}),
    )
    f: float = field(default=0)
    g: date = field(
        default=date(2000, 1, 1),
        metadata=Metadata({"section": ["section", "date", "date"]}),
    )


Numeric = Union[int, float]


@dataclass
class ComplexTypes(FastConfig):
    a: Union[int, float] = 0
    b: Union[str, int | float] = 0
    c: Optional[int] = field(
        default=None, metadata=Metadata({"section": ["section", "optional_int"]})
    )
    d: dict[str, dict[str, int]] = field(
        default_factory=dict, metadata=Metadata({"section": ["section", "dict"]})
    )
    e: Any = 0
    f: Numeric = field(default=0, metadata=Metadata({"section": ["numeric"]}))


class TestFastConfig(unittest.TestCase):
    def test_asdict(self) -> None:
        config = BasicTypes(
            a={"first": "1", "second": "2"},
            b=True,
            c=42,
            d="str",
            e=[1, 2, 3],
            f=0,
            g=date(1979, 5, 27),
        )
        self.assertEqual(
            config.to_dict(),
            {
                "a": {"first": "1", "second": "2"},
                "b": True,
                "c": 42,
                "d": "str",
                "e": [1, 2, 3],
                "f": 0.0,
                "g": date(1979, 5, 27),
            },
        )


class TestConfigBuilder(unittest.TestCase):
    def test_toml_build(self) -> None:
        # basic types
        basic_config: BasicTypes = ConfigBuilder.build(
            "tests/fixtures/basic_type.toml", BasicTypes
        )
        self.assertEqual(
            basic_config,
            BasicTypes(
                a={"first": "1", "second": "2"},
                b=True,
                c=42,
                d="str",
                e=[1, 2, 3],
                f=0,
                g=date(1979, 5, 27),
            ),
        )

        # complex types
        complex_config: ComplexTypes = ConfigBuilder.build(
            "tests/fixtures/complex_type.toml", ComplexTypes
        )

        self.assertEqual(
            complex_config,
            ComplexTypes(
                a=0,
                b="apple",
                c=None,
                d={"numeric": {"one": 1, "zero": 0}},
                e="Any",
                f=42,
            ),
        )

        # open not found file
        with self.assertRaises(FileNotFoundError) as fe:
            ConfigBuilder.build("not_exist.txt", BasicTypes)
        self.assertEqual(str(fe.exception), "not_exist.txt is not found")

        # invalid class
        with self.assertRaises(InvalidConfigError) as ic:
            ConfigBuilder.build("tests/fixtures/basic_type.toml", int)  # type: ignore
        self.assertEqual(
            str(ic.exception), "must be of type FastConfig or an instance of FastConfig"
        )

    def test_toml_update(self) -> None:
        config = ConfigBuilder.build("tests/fixtures/basic_type.toml", BasicTypes())
        self.assertEqual(
            config,
            BasicTypes(
                a={"first": "1", "second": "2"},
                b=True,
                c=42,
                d="str",
                e=[1, 2, 3],
                f=0,
                g=date(1979, 5, 27),
            ),
        )

        # complex types
        complex_config: ComplexTypes = ConfigBuilder.build(
            "tests/fixtures/complex_type.toml", ComplexTypes()
        )

        self.assertEqual(
            complex_config,
            ComplexTypes(
                a=0,
                b="apple",
                c=None,
                d={"numeric": {"one": 1, "zero": 0}},
                e="Any",
                f=42,
            ),
        )

    def test_json_build(self) -> None:
        config: BasicTypes = ConfigBuilder.build(
            "tests/fixtures/basic_type.json", BasicTypes
        )
        self.assertEqual(
            config,
            BasicTypes(
                a={"first": "1", "second": "2"},
                b=True,
                c=42,
                d="str",
                e=[1, 2, 3],
                f=0,
                g=date(1979, 5, 27),
            ),
        )

        complex_config: ComplexTypes = ConfigBuilder.build(
            "tests/fixtures/complex_type.json", ComplexTypes
        )

        self.assertEqual(
            complex_config,
            ComplexTypes(
                a=0,
                b="apple",
                c=None,
                d={"numeric": {"one": 1, "zero": 0}},
                e="Any",
                f=42,
            ),
        )

    def test_json_update(self) -> None:
        builder = ConfigBuilder()
        config: BasicTypes = builder.build(
            "tests/fixtures/basic_type.json", BasicTypes()
        )
        self.assertEqual(
            config,
            BasicTypes(
                a={"first": "1", "second": "2"},
                b=True,
                c=42,
                d="str",
                e=[1, 2, 3],
                f=0,
                g=date(1979, 5, 27),
            ),
        )

        complex_config: ComplexTypes = ConfigBuilder.build(
            "tests/fixtures/complex_type.json", ComplexTypes()
        )

        self.assertEqual(
            complex_config,
            ComplexTypes(
                a=0,
                b="apple",
                c=None,
                d={"numeric": {"one": 1, "zero": 0}},
                e="Any",
                f=42,
            ),
        )


if __name__ == "__main__":
    unittest.main()
