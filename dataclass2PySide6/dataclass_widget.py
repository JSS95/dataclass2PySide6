import dataclasses
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QLineEdit,
    QGroupBox)
from .datawidgets import type2Widget
from typing import Dict


__all__ = [
    "DataclassWidget"
]


@dataclasses.dataclass
class _DefaultDataclass:
    """
    Default empty dataclass for uninitialized :class:`DataclassWidget`.
    """
    pass


class DataclassWidget(QWidget):
    """
    Widget which represents the fields of dataclass type.

    Standard way to construct this widget is by :meth:`fromDataclass`
    class method.

    Subclass may redefine :meth:`field2Widget` method to change the
    subwidget constructed by the field. Every subwidget must have
    ``dataValue()`` method which returns the current value,
    ``dataValueChanged`` signal which emits the changed value,
    and ``setDataValue()`` slot which updates the current value.

    :meth:`currentData` returns the current states of the widgets as
    dataclass instance. :meth:`applyData` updates the current states of
    the widgets with dataclass instance.

    Examples
    ========

    >>> import dataclasses
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import DataclassWidget
    >>> @dataclasses.dataclass
    ... class DataClass:
    ...     a: bool
    ...     b: int
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = DataclassWidget.fromDataclass(DataClass)
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP
    """

    dataChanged = Signal()

    @classmethod
    def fromDataclass(cls, datacls: type) -> "DataclassWidget":
        """
        Construct the widget using the fields from the dataclass.

        Parameters
        ==========

        datacls
            Dataclass type object

        """
        obj = cls()
        obj._dataclass_type = datacls
        fields = dataclasses.fields(datacls)
        obj._widgets = {f.name: obj.field2Widget(f) for f in fields}
        obj.initWidgets()
        obj.initUI()
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = _DefaultDataclass
        self._widgets = {}

    def field2Widget(self, field: dataclasses.Field) -> QWidget:
        """Return a widget for *field*."""
        widget = type2Widget(field.type)
        default = field.default

        if isinstance(widget, QCheckBox):
            widget.setText(field.name)
        elif isinstance(widget, QLineEdit):
            widget.setPlaceholderText(field.name)
        elif isinstance(widget, QGroupBox):
            widget.setTitle(field.name)

        if default != dataclasses.MISSING:
            widget.setDataValue(default)

        return widget

    def dataclassType(self) -> type:
        """Dataclass type which is used to construct *self*."""
        return self._dataclass_type

    def widgets(self) -> Dict[str, QWidget]:
        """
        Sub-widgets which represent the fields of :meth:`dataclassType`.
        """
        return self._widgets

    def initWidgets(self):
        """Initialize the widgets in :meth:`widgets`."""
        for widget in self.widgets().values():
            widget.dataValueChanged.connect(self.emitDataChanged)

    def initUI(self):
        """Initialize the UI with :meth:`widgets`."""
        layout = QVBoxLayout()
        for widget in self.widgets().values():
            layout.addWidget(widget)
        self.setLayout(layout)

    def emitDataChanged(self):
        self.dataChanged.emit()

    def currentData(self) -> object:
        """
        Return the current state of widgets as dataclass instance.

        Returns
        =======

        data
            Dataclass instance

        """
        args = {name: w.dataValue() for (name, w) in self.widgets().items()}
        data = self.dataclassType()(**args)
        return data

    def applyData(self, data: object):
        """
        Apply the dataclass instance to data widgets states.

        Parameters
        ==========

        data
            Dataclass instance

        """
        for name, w in self.widgets().items():
            w.setDataValue(getattr(data, name))
