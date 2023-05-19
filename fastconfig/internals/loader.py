"""this module provides `_FileLoader`."""
import json
from typing import Any

import toml

from fastconfig.exception import InvalidConfigError


class _FileLoader:
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
        try:
            with open(path, "r") as f:
                config = toml.load(f)
        except toml.decoder.TomlDecodeError as e:
            raise InvalidConfigError(str(e))
        return config
