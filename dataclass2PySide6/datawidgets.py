"""
Widgets to represent data of dataclass.

Every widget has following methods and attributes:

* ``dataName()`` : Returns the data name as str
* ``setDataName()`` : Set the data name
* ``dataValue()`` : Returns the data value in correct type
* ``dataValueChanged`` : Signal which emits the changed value
* ``setDataValue()`` : Set the current state of the widget

"""
from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (QWidget, QCheckBox, QLineEdit, QGroupBox,
    QHBoxLayout)
from typing import List


__all__ = [
    "type2Widget",
    "BoolCheckBox",
    "IntLineEdit",
    "FloatLineEdit",
    "StrLineEdit",
    "TupleGroupBox",
]


def type2Widget(type_or_annot) -> QWidget:
    """
    Return the widget instance for given type annotation.

    """
    if isinstance(type_or_annot, type) and issubclass(type_or_annot, bool):
        return BoolCheckBox()
    if isinstance(type_or_annot, type) and issubclass(type_or_annot, int):
        return IntLineEdit()
    if isinstance(type_or_annot, type) and issubclass(type_or_annot, float):
        return FloatLineEdit()
    if isinstance(type_or_annot, type) and issubclass(type_or_annot, str):
        return StrLineEdit()
    if getattr(type_or_annot, "__origin__", None) is tuple: # Tuple
        args = getattr(type_or_annot, "__args__", None)
        if args is None:
            raise TypeError("%s does not have argument type" % type_or_annot)
        if Ellipsis in args:
            txt = "Number of arguments of %s not fixed" % type_or_annot
            raise TypeError(txt)
        widgets = [type2Widget(arg) for arg in args]
        return TupleGroupBox.fromWidgets(widgets)
    raise TypeError("Unknown type or annotation : %s" % type_or_annot)


class BoolCheckBox(QCheckBox):
    """
    Checkbox for boolean value.

    :meth:`dataValue` returns the current boolean value.

    When the check state is changed, :attr:`dataValueChanged` signal is
    emiited.

    :meth:`setDataValue` checks and unchecks the checkbox.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import BoolCheckBox
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = BoolCheckBox()
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """
    dataValueChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.stateChanged.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.text()

    def setDataName(self, name: str):
        self.setText(name)

    def dataValue(self) -> bool:
        return self.isChecked()

    def setDataValue(self, value: bool):
        self.setChecked(value)

    def emitDataValueChanged(self, state: int):
        self.dataValueChanged.emit(bool(state))


class IntLineEdit(QLineEdit):
    """
    Line edit for integer value.

    :meth:`dataValue` returns the current integer value. The default
    value is zero.

    The validator is set as ``QIntValidator``. When text is changed or
    edited, :attr:`dataValueChanged` or :attr:`dataValueEdited`
    signals are emitted.

    :meth:`setDataValue` changes the text.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import IntLineEdit
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = IntLineEdit()
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP
    """
    dataValueChanged = Signal(int)
    dataValueEdited = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QIntValidator())
        self.setDefaultDataValue(0)

        self.textChanged.connect(self.emitDataValueChanged)
        self.textEdited.connect(self.emitDataValueEdited)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)

    def defaultDataValue(self) -> int:
        """
        Default value for empty text.

        This is different from the default value of dataclass field,
        which is used to initialize the widget text.
        """
        return self._default_data_value

    def setDefaultDataValue(self, val: int):
        self._default_data_value = int(val)

    def dataValue(self) -> int:
        text = self.text()
        val = int(text) if text else self.defaultDataValue()
        return val

    def setDataValue(self, value: int):
        self.setText(str(value))

    def emitDataValueChanged(self, text: str):
        val = int(text) if text else self.defaultDataValue()
        self.dataValueChanged.emit(val)

    def emitDataValueEdited(self, text: str):
        val = int(text) if text else self.defaultDataValue()
        self.dataValueEdited.emit(val)


class FloatLineEdit(QLineEdit):
    """
    Line edit for float value.

    :meth:`dataValue` returns the current float value. The default
    value is zero.

    The validator is set as ``QDoubleValidator``. When text is changed
    or edited, :attr:`dataValueChanged` or :attr:`dataValueEdited`
    signals are emitted.

    :meth:`setDataValue` changes the text.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import FloatLineEdit
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = FloatLineEdit()
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP
    """
    dataValueChanged = Signal(float)
    dataValueEdited = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QDoubleValidator())
        self.setDefaultDataValue(float(0))

        self.textChanged.connect(self.emitDataValueChanged)
        self.textEdited.connect(self.emitDataValueEdited)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)

    def defaultDataValue(self) -> float:
        """
        Default value for empty text.

        This is different from the default value of dataclass field,
        which is used to initialize the widget text.
        """
        return self._default_data_value

    def setDefaultDataValue(self, val: float):
        self._default_data_value = float(val)

    def dataValue(self) -> float:
        text = self.text()
        val = float(text) if text else self.defaultDataValue()
        return val

    def setDataValue(self, value: float):
        self.setText(str(value))

    def emitDataValueChanged(self, text: str):
        val = float(text) if text else self.defaultDataValue()
        self.dataValueChanged.emit(val)

    def emitDataValueEdited(self, text: str):
        val = float(text) if text else self.defaultDataValue()
        self.dataValueEdited.emit(val)


class StrLineEdit(QLineEdit):
    """
    Line edit for str value.

    :meth:`dataValue` returns the current str value.

    When text is changed or edited, :attr:`dataValueChanged` or
    :attr:`dataValueEdited` signals are emitted.

    :meth:`setDataValue` changes the text.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import StrLineEdit
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = StrLineEdit()
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP
    """
    dataValueChanged = Signal(str)
    dataValueEdited = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.textChanged.connect(self.emitDataValueChanged)
        self.textEdited.connect(self.emitDataValueEdited)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)

    def dataValue(self) -> str:
        return self.text()

    def setDataValue(self, value: str):
        self.setText(str(value))

    def emitDataValueChanged(self, text: str):
        self.dataValueChanged.emit(str(text))

    def emitDataValueEdited(self, text: str):
        self.dataValueEdited.emit(str(text))


class TupleGroupBox(QGroupBox):
    """
    Widget to represent the tuple data with fixed number of items.

    Standard way to construct this widget is by :meth:`fromWidgets`
    class method. Widgets must be other data widget, e.g.
    :class:`IntLineEdit` or :class:`FloatLineEdit`.

    :meth:`dataValue` returns the current tuple value.

    When data value of subwidgets is changed, :attr:`dataValueChanged`
    signal is emiited.

    :meth:`setDataValue` changes the values of subwidgets

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import (BoolCheckBox, IntLineEdit,
    ...     TupleGroupBox)
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widgets = [BoolCheckBox(), IntLineEdit()]
    ...     widget = TupleGroupBox.fromWidgets(widgets)
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """
    dataValueChanged = Signal(tuple)

    @classmethod
    def fromWidgets(cls, widgets: List[QWidget]) -> "TupleGroupBox":
        obj = cls()
        obj._widgets = widgets
        obj.initWidgets()
        obj.initUI()
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets = []

    def dataName(self) -> str:
        return self.title()

    def setDataName(self, name: str):
        self.setTitle(name)

    def widgets(self) -> List[QWidget]:
        return self._widgets

    def initWidgets(self):
        for widget in self.widgets():
            widget.dataValueChanged.connect(self.emitDataValueChanged)

    def initUI(self):
        layout = QHBoxLayout()
        for widget in self.widgets():
            layout.addWidget(widget)
        self.setLayout(layout)

    def dataValue(self) -> tuple:
        return tuple(widget.dataValue() for widget in self.widgets())

    def setDataValue(self, value: tuple):
        for w, v in zip(self.widgets(), value):
            w.setDataValue(v)
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        value = self.dataValue()
        self.dataValueChanged.emit(value)
