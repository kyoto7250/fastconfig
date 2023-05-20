[![](https://img.shields.io/pypi/pyversions/fastconfig)](https://pypi.org/project/fastconfig/)
[![](https://img.shields.io/pypi/v/fastconfig)](https://pypi.org/project/fastconfig/)
[![](https://img.shields.io/pypi/l/fastconfig)](https://github.com/kyoto7250/fastconfig/blob/main/LICENSE)
![](https://img.shields.io/github/actions/workflow/status/kyoto7250/fastconfig/lint_and_test.yml)
[![](https://img.shields.io/website?down_message=offline&up_color=blue&up_message=online&url=https%3A%2F%2Fkyoto7250.github.io%2Ffastconfig%2F)](https://kyoto7250.github.io/fastconfig/)

# fastconfig
A lightweight way to find the project root and load config in `python3`.
current support is `3.9`, `3.10`, `3.11`.

This library provides two functionalities:

* A function to search for files while traversing up to the project root.
    - `fastconfig.find_project_root`
    - `fastconfig.is_project_root`
    - `fastconfig.search`
* A function to directly build a class from a configuration file.
    - `fastconfig.config.FastConfig`
      * `build`
      * `to_dict`


## Install

```bash
pip install fastconfig
```

## Usage

- `example.json`
```json
{
    "setting_path": "setting_path",
    "section": {
        "numeric": 42
    }
}
```

- `other.toml`
```toml
setting_path = "setting_path"
[section]
numeric = 24
```

```python
# main.py
import fastconfig
from fastconfig.config import FastConfig, fc_field
from fastconfig.exception import FastConfigError
from dataclasses import field, dataclass


@dataclass
class Config(FastConfig):
    result: int = fc_field(key="section.numeric", default=-1)
    # If metadata does not exist, it is searched by variable name
    setting_path: str = fc_field(default="default")
    # Type checking is done based on the type of dataclass. Type checking is recursive.
    dic: dict[str, int] = fc_field(key="section", default_factory=dict)


if path := fastconfig.search("example.json"):
    try:
        # build instance
        config = Config.build(path)
        assert config == Config(
            result=42, setting_path="setting_path", dic={"numeric": 42}
        )
    except FastConfigError:
        raise RuntimeError
else:
    config = Config()

if other_path := fastconfig.search("other.toml"):
    # can update config
    config = Config.build(other_path, config)
    assert config == Config(result=24, setting_path="setting_path", dic={"numeric": 24})
```

## Motivation

In many projects, it is common to write configuration files, read them in code, and build Config classes. I created this library to enable these functions to be implemented by simply defining a class and specifying a file name (such as pyproject.toml).

## Contribution
If you have suggestions for features or improvements to the code, please feel free to create an issue first.
