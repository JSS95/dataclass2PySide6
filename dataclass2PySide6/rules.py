"""
Functions to convert dataclass field to QWidget.
"""
import dataclasses
from PySide6.QtWidgets import QCheckBox, QLineEdit
from .widgets import IntLineEdit, FloatLineEdit


__all__ = [
    "bool2QCheckBox",
    "int2LineEdit",
    "float2LineEdit",
    "str2LineEdit",
]


def bool2QCheckBox(field: dataclasses.Field):
    widget = QCheckBox()
    widget.setCheckable(True)
    widget.setText(field.name)
    default = field.default
    if default != dataclasses.MISSING:
        widget.setChecked(bool(default))
    return widget


def int2LineEdit(field: dataclasses.Field):
    widget = IntLineEdit()
    widget.setPlaceholderText(field.name)
    default = field.default
    if default != dataclasses.MISSING:
        widget.setText(str(default))
    return widget


def float2LineEdit(field: dataclasses.Field):
    widget = FloatLineEdit()
    widget.setPlaceholderText(field.name)
    default = field.default
    if default != dataclasses.MISSING:
        widget.setText(str(default))
    return widget


def str2LineEdit(field: dataclasses.Field):
    widget = QLineEdit()
    widget.setPlaceholderText(field.name)
    default = field.default
    if default != dataclasses.MISSING:
        widget.setText(str(default))
    return widget
