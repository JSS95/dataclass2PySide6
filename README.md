Python package to dynamically create PySide6 widgets from dataclass

# Introduction

dataclass2PySide6 is a package which provides widgets to represent `dataclass` instance as `PySide6` GUI.

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

```python
from PySide6.QtWidgets import QApplication
import sys
from dataclass2PySide6 import DataclassWidget

app = QApplication(sys.argv)
widget = DataclassWidget.fromDataclass(DataClass)
widget.show()
app.exec()
app.quit()
```

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

`DataclassWidget` is a widget for single dataclass type.
For multiple dataclass types in one widget, `StackedDataclassWidget` and `TabDataclassWidget` are provided.

## Single dataclass

`DataclassWidget` is the core object of `dataclass2PySide6`. It contains subwidgets which represent each fields of the dataclass.

User may subclass `DataclassWidget` to define own datclass widget. Refer to the docstring for detailed description.

### Creating widget

To construct `DataclassWidget`, pass dataclass type object to `DataclassWidget.fromDataclass()` method.

To construct suitable widget for each field, `DataclassWidget` searches for `Qt_typehint` [metadata](https://docs.python.org/3/library/dataclasses.html#dataclasses.field).
Its key must be the type annotation, not necessarily identical to `type` attribute of the field.

For example,

```python
from dataclasses import dataclass, field
from typing import Union

@dataclass
class DataClass:
    x: Union[int, float] = field(metadata=dict(Qt_typehint=float))
```

If `Qt_typehint` does not exist, it uses `type` attribute of the field as a fallback.

Currently supported types are:

1. `Enum` : converted to combo box
2. `bool` : converted to check box (`Union` with `None` allowed)
3. `int` and `float` : converted to line edit with validator (`Union` with `None` allowed)
4. `str` : converted to line edit
5. `Tuple` : converted to group box if element types are supported

### Getting data value

When data from any subwidget changes, `DataclassWidget.dataValueChanged` signal emits the new dataclass instance with current value.
For check box or combo box, this is when the current selection changes. For line edit, this is when editing is finished.

`DataclassWidget.dataValue()` method returns the new dataclass instance with current value.

### Setting data value

`DataclassWidget.setDataValue()` method updates the subwidget data with new dataclass instance.

## Multiple dataclasses

`StackedDataclassWidget` and `TabDataclassWidget` provide multiple `DataclassWidget` in one widget.

Both classes provide `addDataclass()` method to add new widget for dataclass, and `indexOf()` method to search widget for dataclass.
When current widget's value is changed, `dataValuechanged` signal emits the new dataclass instance with current value.
