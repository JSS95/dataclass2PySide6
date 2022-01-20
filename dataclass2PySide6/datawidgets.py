"""
Widgets to represent data of dataclass.

Every widget has following methods and attributes:

* ``dataName()``: Returns the data name as str
* ``setDataName()``: Set the data name
* ``dataValue()``: Returns the data value in correct type
* ``dataValueChanged``: Signal which emits the changed value
* ``setDataValue()``: Set the current state of the widget

"""
from enum import Enum
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (QWidget, QCheckBox, QLineEdit, QComboBox,
    QGroupBox, QHBoxLayout)
from typing import List, Optional, Union


__all__ = [
    "type2Widget",
    "BoolCheckBox",
    "MISSING",
    "IntLineEdit",
    "FloatLineEdit",
    "StrLineEdit",
    "TupleGroupBox",
    "EnumComboBox",
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
    if isinstance(type_or_annot, type) and issubclass(type_or_annot, Enum):
        return EnumComboBox.fromEnum(type_or_annot)
    origin = getattr(type_or_annot, '__origin__', None)
    if origin is tuple: # Tuple
        args = getattr(type_or_annot, '__args__', None)
        if args is None:
            raise TypeError('%s does not have argument type' % type_or_annot)
        if Ellipsis in args:
            txt = 'Number of arguments of %s not fixed' % type_or_annot
            raise TypeError(txt)
        widgets = [type2Widget(arg) for arg in args]
        return TupleGroupBox.fromWidgets(widgets)
    elif origin is Union:
        args = [a for a in type_or_annot.__args__ if a is not type(None)]
        if len(args) > 1:
            msg = f'Cannot convert Union with multiple types: {type_or_annot}'
            raise TypeError(msg)
        arg, = args
        if isinstance(arg, type) and issubclass(arg, bool):
            ret = BoolCheckBox()
            ret.setTristate(True)
            return ret
        if isinstance(arg, type) and issubclass(arg, (int, float)):
            raise NotImplementedError
    raise TypeError('Unknown type or annotation: %s' % type_or_annot)


class BoolCheckBox(QCheckBox):
    """
    Checkbox for fuzzy boolean value. If tristate is allowed, boolean
    value and ``None`` are allowed for data. If not, only boolean value
    is allowed.

    :meth:`dataValue` returns the current value.

    When the check state is changed, :attr:`dataValueChanged` signal is
    emiited.

    :meth:`setDataValue` changes the check state of the checkbox.

    Examples
    ========

    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import BoolCheckBox
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = BoolCheckBox()
    ...     widget.setTristate(True)
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """
    dataValueChanged = Signal(object) # bool or None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.stateChanged.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.text()

    def setDataName(self, name: str):
        self.setText(name)
        self.setToolTip(name)

    def dataValue(self) -> bool:
        checkstate = self.checkState()
        if checkstate == Qt.Checked:
            state = True
        elif checkstate == Qt.Unchecked:
            state = False
        else:
            state = None
        return state

    def setDataValue(self, value: Union[bool, None]):
        if value is True:
            state = Qt.Checked
        elif value is False:
            state = Qt.Unchecked
        else:
            state = Qt.PartiallyChecked
        self.setCheckState(state)

    def emitDataValueChanged(self, checkstate: Qt.CheckState):
        if checkstate == Qt.Checked:
            state = True
        elif checkstate == Qt.Unchecked:
            state = False
        else:
            state = None
        self.dataValueChanged.emit(state)


class _MISSING_TYPE:
    """Sentinel object to detect if the default value is set or not."""
    pass

MISSING = _MISSING_TYPE()

class IntLineEdit(QLineEdit):
    """
    Line edit for integer value.

    :meth:`dataValue` returns the integer value from current text using
    :meth:`valueFromText`.

    The validator is ``QIntValidator``. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. Because of the
    validator, the signal is not emitted for invalid text.

    :meth:`setDataValue` changes the text and emits the signal.

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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QIntValidator())
        self.setDefaultDataValue(MISSING)

        self.editingFinished.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def valueFromText(self, text: str) -> int:
        """
        Convert the text to int value.

        If the text is empty and no default value is set, raise
        ``TypeError``.
        """
        val = int(text) if text else self.defaultDataValue()
        if val is MISSING:
            name = self.dataName() or str(self)
            raise TypeError('Missing data for %s' % name)
        return val

    def defaultDataValue(self) -> object:
        """
        Default value for empty text.

        If line edit is empty, this value is used instead. ``MISSING``
        indicates no default value, where ``TypeError`` is raised for
        missing value.
        """
        return self._default_data_value

    def setDefaultDataValue(self, val: object):
        self._default_data_value = val

    def dataValue(self) -> int:
        text = self.text()
        val = self.valueFromText(text)
        return val

    def setDataValue(self, value: int):
        if value == self.defaultDataValue():
            self.setText('')
        else:
            self.setText(str(value))
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        text = self.text()
        val = self.valueFromText(text)
        self.dataValueChanged.emit(val)


class FloatLineEdit(QLineEdit):
    """
    Line edit for float value.

    :meth:`dataValue` returns the float value from current text using
    :meth:`valueFromText`.

    The validator is ``QDoubleValidator``. When editing is finished,
    :attr:`dataValueChanged` signal is emitted. Because of the
    validator, the signal is not emitted for invalid text.

    :meth:`setDataValue` changes the text and emits the signal.

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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QDoubleValidator())
        self.setDefaultDataValue(None)

        self.editingFinished.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def valueFromText(self, text: str) -> float:
        """
        Convert the text to float value.

        If the text is empty and no default value is set, raise
        ``TypeError``.
        """
        val = float(text) if text else self.defaultDataValue()
        if val is None:
            name = self.dataName() or str(self)
            raise TypeError('Missing data for %s' % name)
        return val

    def defaultDataValue(self) -> Optional[float]:
        """
        Default value for empty text.

        If line edit is empty, this value is used instead. ``None``
        indicates no default value, where ``TypeError`` is raised for
        missing value.
        """
        return self._default_data_value

    def setDefaultDataValue(self, val: Optional[float]):
        if val is None:
            self._default_data_value = None
        else:
            self._default_data_value = float(val)

    def dataValue(self) -> float:
        text = self.text()
        val = self.valueFromText(text)
        return val

    def setDataValue(self, value: float):
        self.setText(str(value))
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        text = self.text()
        val = self.valueFromText(text)
        self.dataValueChanged.emit(val)


class StrLineEdit(QLineEdit):
    """
    Line edit for string value.

    :meth:`dataValue` returns the current string value.

    When editing is finished, :attr:`dataValueChanged` signal is
    emitted.

    :meth:`setDataValue` changes the text and emits the signal.

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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.editingFinished.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> str:
        return self.text()

    def setDataValue(self, value: str):
        self.setText(str(value))
        self.emitDataValueChanged()

    def emitDataValueChanged(self):
        self.dataValueChanged.emit(self.text())


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
    def fromWidgets(cls, widgets: List[QWidget]) -> 'TupleGroupBox':
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
        self.setToolTip(name)

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
        try:
            value = self.dataValue()
            self.dataValueChanged.emit(value)
        except (ValueError, TypeError):
            pass


class EnumComboBox(QComboBox):
    """
    Combo box for enum type.

    Standard way to construct this widget is by :meth:`fromEnum` class
    method.

    :meth:`fromEnum` instances are stored in the data of each item as
    ``Qt.UserRole``.

    :meth:`dataValue` returns the enum instance in current item. If
    current item is invalid, return the first item.

    When current item is changed, :attr:`dataValueChanged` signal is
    emiited.

    :meth:`setDataValue` sets the current item to the one which has
    the enum instance as item.

    Examples
    ========

    >>> from enum import Enum
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import EnumComboBox
    >>> class MyEnum(Enum):
    ...     x = 1
    ...     y = 2
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = EnumComboBox.fromEnum(MyEnum)
    ...     geometry = widget.screen().availableGeometry()
    ...     widget.resize(geometry.width() / 3, geometry.height() / 2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """
    dataValueChanged = Signal(Enum)

    @classmethod
    def fromEnum(cls, enum: type) -> 'EnumComboBox':
        obj = cls()
        for e in enum:
            obj.addItem(e.name, userData=e)
        obj.setCurrentIndex(-1)
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentIndexChanged.connect(self.emitDataValueChanged)

    def dataName(self) -> str:
        return self.placeholderText()

    def setDataName(self, name: str):
        self.setPlaceholderText(name)
        self.setToolTip(name)

    def dataValue(self) -> Enum:
        index = self.currentIndex()
        if index == -1:
            index = 0
        return self.itemData(index)

    def setDataValue(self, value: Enum):
        index = self.findData(value)
        self.setCurrentIndex(index)

    def emitDataValueChanged(self, index: int):
        if index != -1:
            self.dataValueChanged.emit(self.itemData(index))
