from PySide6.QtCore import Qt
import pytest
from dataclass2PySide6 import (type2Widget, BoolCheckBox, IntLineEdit,
    FloatLineEdit, StrLineEdit, TupleGroupBox)
from typing import Tuple


def test_type2Widget(qtbot):
    assert isinstance(type2Widget(bool), BoolCheckBox)
    assert isinstance(type2Widget(int), IntLineEdit)
    assert isinstance(type2Widget(float), FloatLineEdit)
    assert isinstance(type2Widget(str), StrLineEdit)

    with pytest.raises(TypeError):
        type2Widget(Tuple)
    with pytest.raises(TypeError):
        type2Widget(Tuple[int, ...])
    tuplegbox1 = type2Widget(Tuple[bool, int, float, str])
    assert isinstance(tuplegbox1.widgets()[0], BoolCheckBox)
    assert isinstance(tuplegbox1.widgets()[1], IntLineEdit)
    assert isinstance(tuplegbox1.widgets()[2], FloatLineEdit)
    assert isinstance(tuplegbox1.widgets()[3], StrLineEdit)
    tuplegbox2 = type2Widget(Tuple[bool, Tuple[int]])
    assert isinstance(tuplegbox2.widgets()[0], BoolCheckBox)
    assert isinstance(tuplegbox2.widgets()[1], TupleGroupBox)
    assert isinstance(tuplegbox2.widgets()[1].widgets()[0], IntLineEdit)


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


def test_TupleGroupBox(qtbot):
    widgets = [IntLineEdit(), FloatLineEdit()]
    widget = TupleGroupBox.fromWidgets(widgets)

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == (42, 0.0)):
        widget.widgets()[0].setDataValue(42)
    assert widget.dataValue() == (42, 0.0)
