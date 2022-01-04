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
    edited, ``valueChanged`` and ``valueEdited`` signals are emitted.

    :meth:`value()` returns the current integer value, or ``None`` if
    the text is empty.

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
    valueChanged = Signal(int)
    valueEdited = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QIntValidator())
        self.textChanged.connect(self.emitValueChanged)
        self.textEdited.connect(self.emitValueEdited)

    def value(self) -> Union[int, None]:
        text = self.text()
        if text:
            return int(text)

    def emitValueChanged(self, text: str):
        if text:
            self.valueChanged.emit(int(text))

    def emitValueEdited(self, text: str):
        if text:
            self.valueEdited.emit(int(text))


class FloatLineEdit(QLineEdit):
    """
    Line edit for float value.

    The validator is set as ``QDoubleValidator``. When text is changed
    or edited, ``valueChanged`` and ``valueEdited`` signals are emitted.

    :meth:`value()` returns the current float value, or ``None`` if the
    text is empty.

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
    valueChanged = Signal(float)
    valueEdited = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setValidator(QDoubleValidator())
        self.textChanged.connect(self.emitValueChanged)
        self.textEdited.connect(self.emitValueEdited)

    def value(self) -> Union[float, None]:
        text = self.text()
        if text:
            return float(text)

    def emitValueChanged(self, text: str):
        if text:
            self.valueChanged.emit(float(text))

    def emitValueEdited(self, text: str):
        if text:
            self.valueEdited.emit(float(text))
