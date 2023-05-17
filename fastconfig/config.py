import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, List, Mapping, Set, Type, TypedDict, TypeVar, Union

from fastconfig.exception import InvalidConfigError
from fastconfig.internals.loader import FileLoader
from fastconfig.internals.validator import DEFAULT_VALUE, Validator


@dataclass
class FastConfig:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


X = TypeVar("X", bound=FastConfig)

if sys.version_info > (3, 11):
    from typing import NotRequired, Required

    class Metadata(TypedDict):
        section: Required[str | List[str]]
        choice: NotRequired[List[Any] | Set[str]]
        validate: NotRequired[Callable[..., bool]]

else:

    class Metadata(Mapping):
        def __init__(self, mapping) -> None:
            self._mapping: dict[str, Any] = {}

            if "section" in mapping:
                self._mapping["section"] = mapping["section"]

            if "choice" in mapping:
                self._mapping["choice"] = mapping["choice"]

            if "validate" in mapping:
                self._mapping["validate"] = mapping["validate"]

        def __getitem__(self, key):
            return self._mapping[key]

        def __len__(self):
            return len(self._mapping)

        def __iter__(self):
            return iter(self._mapping)


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
