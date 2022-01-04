from PySide6.QtCore import Qt
from dataclass2PySide6 import IntLineEdit, FloatLineEdit


def test_IntLineEdit(qtbot):
    widget = IntLineEdit()

    # test valueChanged signal
    with qtbot.waitSignal(widget.valueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        widget.setText("1")
    assert widget.value() == 1

    # test valueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
    assert widget.value() == 1

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 11):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".") # this key is ignored
        qtbot.keyPress(widget, "1")
    assert widget.value() == 11


def test_FloatLineEdit(qtbot):
    widget = FloatLineEdit()

    # test valueChanged signal
    with qtbot.waitSignal(widget.valueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        widget.setText("1.2")
    assert widget.value() == 1.2

    # test valueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, "2")
    assert widget.value() == 1.2

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.valueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, ".") # this key is ignored
        qtbot.keyPress(widget, "2")
    assert widget.value() == 1.2
