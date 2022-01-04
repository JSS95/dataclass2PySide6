from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLineEdit


__all__ = [
    "IntLineEdit",
]


class IntLineEdit(QLineEdit):
    """
    Line edit for integer value.

    The validator is set as ``QIntValidator``. When text is changed or
    edited, ``valueChanged`` and ``valueEdited`` signals are emitted.

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

    def emitValueChanged(self, text: str):
        if text:
            self.valueChanged.emit(int(text))

    def emitValueEdited(self, text: str):
        if text:
            self.valueEdited.emit(int(text))
