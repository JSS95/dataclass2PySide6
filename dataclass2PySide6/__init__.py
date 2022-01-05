from .version import __version__ # noqa

from .datawidgets import (type2Widget, BoolCheckBox, IntLineEdit,
    FloatLineEdit, StrLineEdit, TupleGroupBox)
from .dataclass_widget import DataclassWidget


__all__ = [
    "type2Widget",
    "BoolCheckBox",
    "IntLineEdit",
    "FloatLineEdit",
    "StrLineEdit",
    "TupleGroupBox",

    "DataclassWidget",
]
