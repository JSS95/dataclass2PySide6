from PySide6.QtCore import Qt
from dataclass2PySide6 import IntLineEdit


def test_IntLineEdit(qtbot):
    widget = IntLineEdit()

    # test valueChanged signal
    with qtbot.waitSignal(widget.valueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        widget.setText("1")

    # test valueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 11):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".") # this key is ignored
        qtbot.keyPress(widget, "1")
