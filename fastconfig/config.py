"""this module provides FastConfig class."""
import os
import sys
from dataclasses import MISSING, asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Type, TypeVar, Union

from fastconfig.exception import InvalidConfigError
from fastconfig.internals.loader import _FileLoader
from fastconfig.internals.validator import DEFAULT_VALUE, _Validator

_T = TypeVar("_T")
_Self = TypeVar("_Self", bound="FastConfig")


@dataclass
class FastConfig:
    """this class provides the way to build and update instance from `toml` or `json` format file."""

    @classmethod
    def build(
        cls: Type[_Self], path: Union[str, Path], config: Optional[_Self] = None
    ) -> _Self:
        """
        Read file from path and create/update instance.

        Args:
            path: Union[str, Path]
                a file path to read a config
            config: Optional[_Self]
                an instance inheriting from FastConfig (if updating)
        Returns:
            _Self: an instance inheriting from FastConfig
        """
        if config is None:
            return _FastConfigBuilder.build(path, cls)
        else:
            return _FastConfigBuilder.build(path, config)

    def to_dict(self, use_key: bool = False) -> dict[str, Any]:
        """
        Convert from an instance to dict.

        Args:
            use_key: bool
                Whether to convert to dictionary by class instance name
        Returns:
            dict[str, Any]
        """
        if use_key:
            return asdict(self)

        dic: dict[str, Any] = {}
        for key, f in self.__dataclass_fields__.items():
            metadata: dict[str, Any] = (
                dict(f.metadata) if hasattr(f, "metadata") else {}
            )
            separator = metadata["separator"] if "separator" in metadata else "."
            setting_key: list[str] = (
                metadata["key"].split(separator) if "key" in metadata else [key]
            )
            inside: dict[str, Any] = dic
            for nest_field in setting_key[:-1]:
                if nest_field not in dic:
                    inside[nest_field] = {}
                inside = inside[nest_field]
            inside[setting_key[-1]] = getattr(self, key)
        return dic


if sys.version_info >= (3, 10):

    def fc_field(
        key: Optional[str | int] = None,
        separator: str = ".",
        default: _T = MISSING,
        default_factory: Type[_T] = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: Optional[bool] = None,
        compare: bool = True,
        metadata: Mapping[Any, Any] | None = None,
        kw_only=MISSING,
    ) -> _T:
        """
        Return `dataclass::field`.

        wrapper of `dataclass::field` for FastConfig definition.
        same as `field` except for passing `key` and `separator`.

        Args:
            key: Optional[str | int]
                the name of the key you want to read, divided by `separator` when retrieving data
            separator: str
                Separator for splitting key values, default is `.`

        Returns:
            _T
        """
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
        key: Optional[Union[str, int]] = None,
        separator: str = ".",
        default: _T = MISSING,
        default_factory: Type[_T] = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: Optional[bool] = None,
        compare: bool = True,
        metadata: Optional[Mapping[Any, Any]] = None,
    ) -> _T:
        """
        Return `dataclass::field`.

        wrapper of `dataclass::field` for FastConfig definition.
        same as `field` except for passing `key` and `separator`.

        Args:
            key: Optional[str | int]
                the name of the key you want to read, divided by `separator` when retrieving data
            separator: str
                Separator for splitting key values, default is `.`

        Returns:
            _T
        """
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


class _FastConfigBuilder:
    @classmethod
    def build(cls, path: Union[str, Path], config: Union[_Self, Type[_Self]]) -> _Self:
        if isinstance(path, Path):
            path = str(path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} is not found")

        loader: _FileLoader = _FileLoader()
        data: dict[str, Any] = loader(path)
        if not isinstance(config, type) and isinstance(config, FastConfig):
            return cls._update(config, data)
        elif isinstance(config, type) and issubclass(config, FastConfig):
            return cls._make(config, data)
        else:
            raise InvalidConfigError(
                "must be of type FastConfig or an instance of FastConfig"
            )

    @classmethod
    def _make(
        cls,
        config: Type[_Self],
        setting: dict[str, Any],
    ) -> _Self:
        # check metadata and type hint
        args: dict[str, Any] = {}
        checker: _Validator = _Validator(setting)
        for key, f in config.__dataclass_fields__.items():
            value = checker(key, f)
            if not isinstance(value, DEFAULT_VALUE):
                args[key] = value
        return config(**args)

    @classmethod
    def _update(cls, config: _Self, setting: dict[str, Any]) -> _Self:
        checker: _Validator = _Validator(setting)
        for key, f in config.__dataclass_fields__.items():
            value = checker(key, f, build=False)
            if not isinstance(value, DEFAULT_VALUE):
                setattr(config, key, value)
        return config
