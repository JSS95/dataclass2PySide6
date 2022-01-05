Python package to dynamically create PySide6 widgets from dataclass

# Introduction

dataclass2PySide6 is a package which provides widgets and functions to represent `dataclass` instance as `PySide6` GUI.

For example, here is a simple dataclass:

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DataClass:
    a: bool
    b: int
    c: Tuple[float, Tuple[bool, int]] = (4.2, (True, 99))
```

Dataclass widget can be dynamically created as follows.

<div align="center">
  <img src="https://github.com/JSS95/dataclass2PySide6/raw/master/imgs/example.png"/><br>
</div>

# Installation

Before you install, be careful for other Qt-dependent packages installed in your environment.
For example, non-headless `OpenCV-Python` module modifies the Qt dependency thus making PySide6 unavailable.

`dataclass2PySide6` can be installed using `pip`.

```
$ pip install dataclass2PySide6
```

# How to use

1. Create dataclass widget using ``DataclassWidget.fromDataclass()``.
2. Get current state of widget with ``dataValueChanged`` signal and ``dataValue()`` method.
3. Update the current state of widget with ``setDataValue()`` method.

User may subclass ``DataclassWidget`` to define own datclass widget.
Refer to the docstring for detailed description.
