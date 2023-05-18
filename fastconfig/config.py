import os
import sys
from dataclasses import MISSING, asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Type, TypeVar, Union

from fastconfig.exception import InvalidConfigError
from fastconfig.internals.loader import FileLoader
from fastconfig.internals.validator import DEFAULT_VALUE, Validator


@dataclass
class FastConfig:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


X = TypeVar("X", bound=FastConfig)
T = TypeVar("T")

if sys.version_info >= (3, 10):

    def fc_field(
        key: Optional[str | int] = None,
        separator: str = ".",
        default: T = MISSING,
        default_factory: Type[T] = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: bool | None = None,
        compare: bool = True,
        metadata: Mapping[Any, Any] | None = None,
        kw_only=MISSING,
    ) -> T:
        options: dict[str, Any] = {
            "default": default,
            "default_factory": default_factory,
            "init": init,
            "repr": repr,
            "hash": hash,
            "compare": compare,
            "metadata": metadata if metadata is not None else {},
            "kw_only": kw_only,
        }

        if key is not None:
            options["metadata"]["key"] = key
        options["metadata"]["separator"] = separator
        return field(**options)

else:

    def fc_field(
        key: Optional[str | int] = None,
        separator: str = ".",
        default: T = MISSING,
        default_factory: Type[T] = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: bool | None = None,
        compare: bool = True,
        metadata: Mapping[Any, Any] | None = None,
    ) -> T:
        options: dict[str, Any] = {
            "default": default,
            "default_factory": default_factory,
            "init": init,
            "repr": repr,
            "hash": hash,
            "compare": compare,
            "metadata": metadata if metadata is not None else {},
        }

        if key is not None:
            options["metadata"]["key"] = key
        options["metadata"]["separator"] = separator
        return field(**options)


class ConfigBuilder:
    @classmethod
    def build(cls, path: Union[str, Path], config: Union[X, Type[X]]) -> X:
        if isinstance(path, Path):
            path = str(path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} is not found")

        loader: FileLoader = FileLoader()
        data: dict[str, Any] = loader(path)
        if not isinstance(config, type) and isinstance(config, FastConfig):
            return cls.update(config, data)
        elif isinstance(config, type) and issubclass(config, FastConfig):
            return cls.make(config, data)
        else:
            raise InvalidConfigError(
                "must be of type FastConfig or an instance of FastConfig"
            )

    @classmethod
    def make(
        cls,
        config: Type[X],
        setting: dict[str, Any],
    ) -> X:
        # check metadata and type hint
        args: dict[str, Any] = {}
        checker: Validator = Validator(setting)
        for key, f in config.__dataclass_fields__.items():
            value = checker(key, f)
            if not isinstance(value, DEFAULT_VALUE):
                args[key] = value
        return config(**args)

    @classmethod
    def update(cls, config: X, setting: dict[str, Any]) -> X:
        checker: Validator = Validator(setting)
        for key, f in config.__dataclass_fields__.items():
            value = checker(key, f, build=False)
            if not isinstance(value, DEFAULT_VALUE):
                setattr(config, key, value)
        return config
