"""
Functions to convert dataclass field to QWidget.
"""
import dataclasses
from PySide6.QtWidgets import QCheckBox


__all__ = [
    "bool2QCheckBox",
]


def bool2QCheckBox(field: dataclasses.Field):
    widget = QCheckBox()
    widget.setCheckable(True)
    widget.setText(field.name)
    default = field.default
    if default != dataclasses.MISSING:
        widget.setChecked(bool(default))
    return widget
