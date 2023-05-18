from dataclasses import MISSING, Field
from typing import Any, Optional, Union

from fastconfig.exception import MissingRequiredElementError
from fastconfig.internals.type_checker import TypeChecker


def extract(setting: dict[str, Any], section: Union[str, list[str]]) -> Optional[Any]:
    if isinstance(section, str) and section in setting:
        return setting[section]
    elif isinstance(section, list):
        for element in section:
            if not (isinstance(setting, dict) and element in setting):
                return None
            setting = setting[element]
        return setting
    return None


class DEFAULT_VALUE:
    """
    This class is the dummy object for meaning `use default value`
    """

    pass


class Validator:
    def __init__(self, setting: dict[str, Any]) -> None:
        self.setting: dict[str, Any] = setting
        self.checker: TypeChecker = TypeChecker()

    def __call__(self, key: str, f: Field, build: bool = True) -> Any:
        metadata: dict[str, Any] = dict(f.metadata) if hasattr(f, "metadata") else {}
        separator = metadata["separator"] if "separator" in metadata else "."
        setting_key: str = (
            metadata["key"].split(separator) if "key" in metadata else key
        )
        value: Any = extract(self.setting, setting_key)

        if value is None:
            if (
                isinstance(f.default, type(MISSING))
                and isinstance(f.default_factory, type(MISSING))
                and build
            ):
                # TODO: check default_factry
                raise MissingRequiredElementError(f"key: {key} is not found")
            return DEFAULT_VALUE()

        value = self.checker(key, value, f.type)
        return value
