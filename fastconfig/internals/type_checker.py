"""this module provides _TypeChecker."""
import datetime
from types import GenericAlias
from typing import Any, Type, Union, _SpecialForm, get_args, get_origin

from fastconfig.exception import UnexpectedValueError

DATE_TYPES = [datetime.datetime, datetime.date, datetime.time]


class _TypeChecker:
    def __call__(
        self, key: str, value: Any, typeinfo: Union[type, GenericAlias, _SpecialForm]
    ) -> Any:
        self.value = value
        if not self.check(key, value, typeinfo):
            raise UnexpectedValueError(
                f"{key}: {value} is not valid type. must be of type {typeinfo}"
            )
        return self.value

    def check(
        self, key: str, value: Any, typeinfo: Union[type, GenericAlias, _SpecialForm]
    ) -> bool:
        if typeinfo == Any:
            return True
        outside = get_origin(typeinfo)
        if outside is None:
            if any(typeinfo is ty for ty in DATE_TYPES):
                return self.check_datetime(value, typeinfo)  # type: ignore
            return isinstance(value, typeinfo)  # type: ignore
        return self.check_origin(key, value, typeinfo)

    def check_origin(
        self,
        key: str,
        value: Any,
        typeinfo: Union[type, GenericAlias, _SpecialForm],
    ) -> bool:
        outside = get_origin(typeinfo)
        types = get_args(typeinfo)
        if outside == Union:
            return any(self.check(key, value, ty) for ty in types)
        elif outside == dict:
            k, v = types
            if not isinstance(value, dict):
                return False
            return all(self.check(key, key, k) for key in value.keys()) and all(
                self.check(key, val, v) for val in value.values()
            )
        elif outside == list:
            content = types[0]
            if not isinstance(value, list):
                return False
            return all(self.check(key, val, content) for val in value)
        else:
            raise UnexpectedValueError(f"{typeinfo} is not supported")

    def check_datetime(
        self,
        value: Union[str, datetime.datetime, datetime.date, datetime.time],
        typeinfo: Union[
            Type[datetime.datetime], Type[datetime.date], Type[datetime.time]
        ],
    ) -> Any:
        if type(value) is typeinfo:
            return True

        if isinstance(value, str):
            if typeinfo is datetime.time:
                return False
            try:
                """
                TODO:
                ISO 8601 and RFC 3339 is not compatible
                However, there are few use cases for writing the specified date and time to the setting value,
                so I left it as it is for now.
                """
                value = datetime.datetime.fromisoformat(value)
            except ValueError:
                return False

        if not isinstance(value, datetime.datetime):
            return False

        if typeinfo is datetime.date:
            value = value.date()
        elif typeinfo is datetime.time:
            value = value.time()

        self.value = value
        return True
