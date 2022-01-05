from PySide6.QtCore import Qt
from dataclass2PySide6 import (BoolCheckBox, IntLineEdit, FloatLineEdit,
    StrLineEdit)


def test_BoolCheckBox(qtbot):
    widget = BoolCheckBox()

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val):
        widget.setDataValue(True)
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: not val):
        widget.setDataValue(False)


def test_IntLineEdit(qtbot):
    widget = IntLineEdit()

    # test default data value
    assert widget.dataValue() == 0
    widget.setDefaultDataValue(1)
    assert widget.dataValue() == 1
    widget.setDefaultDataValue(0)

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        widget.setDataValue("1")
    assert widget.dataValue() == 1
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 0):
        widget.setDataValue("")
    assert widget.dataValue() == 0

    # test dataValueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.dataValueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
    assert widget.dataValue() == 1

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.dataValueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 11):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".") # this key is ignored
        qtbot.keyPress(widget, "1")
    assert widget.dataValue() == 11


def test_FloatLineEdit(qtbot):
    widget = FloatLineEdit()

    # test default data value
    assert widget.dataValue() == float(0)
    widget.setDefaultDataValue(float(1))
    assert widget.dataValue() == float(1)
    widget.setDefaultDataValue(float(0))

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        widget.setDataValue("1.2")
    assert widget.dataValue() == 1.2
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == float(0)):
        widget.setDataValue("")
    assert widget.dataValue() == float(0)

    # test dataValueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.dataValueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, "2")
    assert widget.dataValue() == 1.2

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.dataValueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "1")
        qtbot.keyPress(widget, ".")
        qtbot.keyPress(widget, ".") # this key is ignored
        qtbot.keyPress(widget, "2")
    assert widget.dataValue() == 1.2


def test_StrLineEdit(qtbot):
    widget = StrLineEdit()

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == "foo"):
        widget.setDataValue("foo")
    assert widget.dataValue() == "foo"

    # test dataValueEdited signal
    widget.clear()
    with qtbot.waitSignal(widget.dataValueEdited,
                          raising=True,
                          check_params_cb=lambda val: val == "bar"):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, "b")
        qtbot.keyPress(widget, "a")
        qtbot.keyPress(widget, "r")
    assert widget.dataValue() == "bar"
