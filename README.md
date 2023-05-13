# fastconfig
A lightweight way to find the project root and load config


## Abstract

This library provides two functionalities:
(The config function is under development)

* A function to search for files while traversing up to the project root.
    - `fastconfig.find_project_root`
    - `fastconfig.is_project_root`
    - `fastconfig.search`
* A function to directly build a class from a configuration file.


## Install

```bash
pip install fastconfig
```

## Usage


```python
import fastconfig
import pathlib
from typing import Optional

path: Optional[pathlib.Path] = fastconfig.search("pyproject.toml")
if path is not None:
    # TODO: read config
    pass
```

## Motivation

In many projects, it is common to write configuration files, read them in code, and build Config classes. I created this library to enable these functions to be implemented by simply defining a class and specifying a file name (such as pyproject.toml).

## Contribution
If you have suggestions for features or improvements to the code, please feel free to create an issue or pull request.
