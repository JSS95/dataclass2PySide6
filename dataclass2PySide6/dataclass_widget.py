import dataclasses
from PySide6.QtWidgets import QWidget, QVBoxLayout
from .rules import bool2QCheckBox, int2LineEdit, float2LineEdit, str2LineEdit
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
    class method. Subclass may redefine :meth:`field2Widget` method to
    change the subwidget constructed by the field.

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
    ...     c: float
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
        obj.initUI()
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = _DefaultDataclass
        self._widgets = {}

    def field2Widget(self, field: dataclasses.Field) -> QWidget:
        """
        Return a widget for *field*.

        """
        if issubclass(field.type, bool):
            widget = bool2QCheckBox(field)
        elif issubclass(field.type, int):
            widget = int2LineEdit(field)
        elif issubclass(field.type, float):
            widget = float2LineEdit(field)
        elif issubclass(field.type, str):
            widget = str2LineEdit(field)
        else:
            raise TypeError("Unknown type: %s" % field.type)
        return widget

    def dataclassType(self) -> type:
        """
        Dataclass type which is used to construct *self*.

        """
        return self._dataclass_type

    def widgets(self) -> Dict[str, QWidget]:
        """
        Sub-widgets which represent the fields of :meth:`dataclassType`.

        """
        return self._widgets

    def initUI(self):
        """
        Initialize the UI with :meth:`widgets`.

        """
        layout = QVBoxLayout()
        for widget in self.widgets().values():
            layout.addWidget(widget)
        self.setLayout(layout)