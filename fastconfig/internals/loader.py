import json
import sys
from typing import Any

from fastconfig.exception import InvalidConfigError

if sys.version_info >= (3, 11):
    import tomllib
else:
    import toml as tomllib


class FileLoader:
    def __call__(self, path: str) -> dict[str, Any]:
        if path.endswith(".json"):
            return self.load_json(path)
        elif path.endswith(".toml"):
            return self.load_toml(path)
        raise InvalidConfigError("FastConfig only supports json and toml formats now")

    def load_json(self, path: str) -> dict[str, Any]:
        try:
            with open(path, "r") as f:
                config: Any = json.load(f)
            if not isinstance(config, dict):
                config = {"content": config}
            return config
        except json.decoder.JSONDecodeError as e:
            raise InvalidConfigError(str(e))

    def load_toml(self, path: str) -> dict[str, Any]:
        if sys.version_info >= (3, 11):
            try:
                with open(path, "rb") as f:
                    config = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise InvalidConfigError(str(e))
        else:
            try:
                with open(path, "r") as f:
                    config = tomllib.load(f)
            except tomllib.decoder.TomlDecodeError as e:
                raise InvalidConfigError(str(e))
        return config
