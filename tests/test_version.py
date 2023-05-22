import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from fastconfig import FastConfig, __version__, fc_field, search


@dataclass
class Version(FastConfig):
    version: str = fc_field(key="tool.poetry.version")


class TestVersion(unittest.TestCase):
    def test_version(self) -> None:
        pyproject_toml: Optional[Path] = search("pyproject.toml")
        self.assertIsNotNone(pyproject_toml)
        version: Version = Version.build(pyproject_toml)  # type: ignore
        assert version.version == __version__
