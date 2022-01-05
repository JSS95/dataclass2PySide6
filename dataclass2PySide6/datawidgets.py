"""
Widgets to represent data of dataclass.

Every widget has following methods and attributes:

* ``dataValue()`` : Returns the data in correct type
* ``dataValueChanged`` : Signal which emits the changed value
* ``setDataValue()`` : Set the current state of the widget

"""
from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QCheckBox, QLineEdit


__all__ = [
    "BoolCheckBox",
    "IntLineEdit",
    "FloatLineEdit",
    "StrLineEdit",
]


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

    def dataValue(self) -> str:
        return self.text()

    def setDataValue(self, value: str):
        self.setText(str(value))

    def emitDataValueChanged(self, text: str):
        self.dataValueChanged.emit(str(text))

    def emitDataValueEdited(self, text: str):
        self.dataValueEdited.emit(str(text))
