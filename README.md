# fastconfig
A lightweight way to find the project root and load config in python3.
current support is [`3.9`, `3.10`, `3.11`].


## Abstract

This library provides two functionalities:


* A function to search for files while traversing up to the project root.
    - `fastconfig.find_project_root`
    - `fastconfig.is_project_root`
    - `fastconfig.search`
* A function to directly build a class from a configuration file.
    - `fastconfig.config.FastConfig`
    - `fastconfig.config.ConfigBuilder`


## Install

```bash
pip install fastconfig
```

## Usage

### toml

```toml
setting_path = "setting_path"
[section]
numeric = 24
```


```json
{
    "setting_path": "setting_path",
    "section": {
        "numeric": 42
    }
}
```

```python
import fastconfig
from fastconfig.config import FastConfig, ConfigBuilder, Metadata
from fastconfig.exception import FastConfigError
from dataclasses import field, dataclass


@dataclass
class Config(FastConfig):
    result: int = field(
        default=-1, metadata=Metadata({"section": ["section", "numeric"]})
    )
    # If metadata does not exist, it is searched by variable name
    setting_path: str = field(default="default")
    # Type checking is done based on the type of dataclass. Type checking is recursive.
    dic: dict[str, int] = field(
        default_factory=dict, metadata=Metadata({"section": "section"})
    )


if path := fastconfig.search("example.json"):
    try:
        # build instance
        config = ConfigBuilder.build(path, Config)
        assert config == Config(
            result=42, setting_path="setting_path", dic={"numeric": 42}
        )
    except FastConfigError:
        raise RuntimeError
else:
    config = Config()

if other_path := fastconfig.search("other.toml"):
    # can update config
    config = ConfigBuilder.build(other_path, config)
    assert config == Config(result=24, setting_path="setting_path", dic={"numeric": 24})
```

## Motivation

In many projects, it is common to write configuration files, read them in code, and build Config classes. I created this library to enable these functions to be implemented by simply defining a class and specifying a file name (such as pyproject.toml).

## Contribution
If you have suggestions for features or improvements to the code, please feel free to create an issue first.
