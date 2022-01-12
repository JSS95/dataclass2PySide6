from enum import Enum
from PySide6.QtCore import Qt
import pytest
from dataclass2PySide6 import (type2Widget, BoolCheckBox, IntLineEdit,
    FloatLineEdit, StrLineEdit, TupleGroupBox, EnumComboBox)
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
        widget.setChecked(True)
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: not val):
        widget.setChecked(False)


def test_IntLineEdit(qtbot):
    widget = IntLineEdit()

    with pytest.raises(TypeError):
        widget.dataValue()

    # test default data value
    widget.setDefaultDataValue(1)
    assert widget.dataValue() == 1
    widget.setDefaultDataValue(10)
    assert widget.dataValue() == 10

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1):
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == 1

    widget.clear()
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == -1):
        qtbot.keyPress(widget, '-')
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == -1

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 11):
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, '.') # this key is ignored
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == 11


def test_FloatLineEdit(qtbot):
    widget = FloatLineEdit()

    with pytest.raises(TypeError):
        widget.dataValue()

    # test default data value
    widget.setDefaultDataValue(1)
    assert widget.dataValue() == float(1)
    widget.setDefaultDataValue(10)
    assert widget.dataValue() == float(10)

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, '.')
        qtbot.keyPress(widget, '2')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == 1.2

    widget.clear()
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == -1.2):
        qtbot.keyPress(widget, '-')
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, '.')
        qtbot.keyPress(widget, '2')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == -1.2

    # test validator
    widget.clear()
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 1.2):
        qtbot.mouseClick(widget, Qt.LeftButton)
        qtbot.keyPress(widget, '1')
        qtbot.keyPress(widget, '.')
        qtbot.keyPress(widget, '.') # this key is ignored
        qtbot.keyPress(widget, '2')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == 1.2


def test_StrLineEdit(qtbot):
    widget = StrLineEdit()

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == 'foo'):
        qtbot.keyPress(widget, 'f')
        qtbot.keyPress(widget, 'o')
        qtbot.keyPress(widget, 'o')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == 'foo'
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == ''):
        widget.setText('')
        qtbot.keyPress(widget, Qt.Key_Return)
    assert widget.dataValue() == ''


def test_TupleGroupBox(qtbot):
    widgets = [IntLineEdit(), FloatLineEdit()]
    widget = TupleGroupBox.fromWidgets(widgets)

    with pytest.raises(TypeError):
        widget.dataValue()

    # test dataValueChanged signal
    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == (42, 0.0)):
        widget.widgets()[0].setText('42')
        qtbot.keyPress(widget.widgets()[0], Qt.Key_Return)
        widget.widgets()[1].setText('0')
        qtbot.keyPress(widget.widgets()[1], Qt.Key_Return)
    assert widget.dataValue() == (42, 0.0)


def test_EnumComboBox(qtbot):
    class MyEnum(Enum):
        x = 1
        y = 2
        z = 3

    widget = EnumComboBox.fromEnum(MyEnum)
    assert widget.count() == 3
    assert widget.currentIndex() == -1
    assert widget.dataValue() == MyEnum.x

    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == MyEnum.y):
        widget.setDataValue(MyEnum.y)

    with qtbot.waitSignal(widget.dataValueChanged,
                          raising=True,
                          check_params_cb=lambda val: val == MyEnum.z):
        widget.setCurrentIndex(2)

    with qtbot.assertNotEmitted(widget.dataValueChanged):
        widget.setCurrentIndex(-1)
