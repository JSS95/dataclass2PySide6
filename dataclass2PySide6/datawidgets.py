"""
Widgets to represent data of dataclass. Every widget has ``dataValue()``
method which returns the data in correct type.
"""
from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QLineEdit
from typing import Union


__all__ = [
    "IntLineEdit",
    "FloatLineEdit",
]


class IntLineEdit(QLineEdit):
    """
    Line edit for integer value.

    The validator is set as ``QIntValidator``. When text is changed or
    edited, ``dataValueChanged`` and ``dataValueEdited`` signals are
    emitted.

    :meth:`dataValue()` returns the current integer value, or ``None``
    if the text is empty.

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
        self.textChanged.connect(self.emitDataValueChanged)
        self.textEdited.connect(self.emitDataValueEdited)

    def dataValue(self) -> Union[int, None]:
        text = self.text()
        if text:
            return int(text)

    def emitDataValueChanged(self, text: str):
        if text:
            self.dataValueChanged.emit(int(text))

    def emitDataValueEdited(self, text: str):
        if text:
            self.dataValueEdited.emit(int(text))


class FloatLineEdit(QLineEdit):
    """
    Line edit for float value.

    The validator is set as ``QDoubleValidator``. When text is changed
    or edited, ``dataValueChanged`` and ``dataValueEdited`` signals are
    emitted.

    :meth:`dataValue()` returns the current float value, or ``None`` if 
    the text is empty.

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
        self.textChanged.connect(self.emitValueChanged)
        self.textEdited.connect(self.emitValueEdited)

    def dataValue(self) -> Union[float, None]:
        text = self.text()
        if text:
            return float(text)

    def emitValueChanged(self, text: str):
        if text:
            self.dataValueChanged.emit(float(text))

    def emitValueEdited(self, text: str):
        if text:
            self.dataValueEdited.emit(float(text))
