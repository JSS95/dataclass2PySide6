import dataclasses
import pytest
from dataclass2PySide6 import DataclassWidget
from typing import Tuple


@pytest.fixture
def dclswidget(qtbot):

    @dataclasses.dataclass
    class DataClass:
        bool1: bool
        int1: int
        float1: float
        str1: str
        Tuple1: Tuple[bool, int]
        Tuple2: Tuple[bool, Tuple[int]]
        bool2: bool = True
        bool3: bool = False
        int2: int = 42
        float2: float = 4.2
        str2: str = "foo"
        Tuple3: Tuple[bool, int] = (True, 1)
        Tuple4: Tuple[bool, Tuple[int]] = (False, (2,))

    widget = DataclassWidget.fromDataclass(DataClass)
    return widget


def test_DataclassWidget_construction(qtbot, dclswidget):

    widget_bool1 = dclswidget.widgets()["bool1"]
    assert not widget_bool1.isChecked()
    assert widget_bool1.text() == "bool1"

    widget_int1 = dclswidget.widgets()["int1"]
    assert widget_int1.placeholderText() == "int1"
    assert widget_int1.text() == ""
    assert widget_int1.dataValue() == 0

    widget_float1 = dclswidget.widgets()["float1"]
    assert widget_float1.placeholderText() == "float1"
    assert widget_float1.text() == ""
    assert widget_float1.dataValue() == float(0)

    widget_str1 = dclswidget.widgets()["str1"]
    assert widget_str1.placeholderText() == "str1"
    assert widget_str1.text() == ""

    widget_Tuple1 = dclswidget.widgets()["Tuple1"]
    assert widget_Tuple1.title() == "Tuple1"
    assert not widget_Tuple1.widgets()[0].isChecked()
    assert widget_Tuple1.widgets()[1].text() == ""
    assert widget_Tuple1.widgets()[1].dataValue() == 0

    widget_Tuple2 = dclswidget.widgets()["Tuple2"]
    assert not widget_Tuple2.widgets()[0].isChecked()
    assert widget_Tuple2.widgets()[1].widgets()[0].text() == ""
    assert widget_Tuple2.widgets()[1].widgets()[0].dataValue() == 0

    widget_bool2 = dclswidget.widgets()["bool2"]
    assert widget_bool2.isChecked()

    widget_bool3 = dclswidget.widgets()["bool3"]
    assert not widget_bool3.isChecked()

    widget_int2 = dclswidget.widgets()["int2"]
    assert widget_int2.text() == "42"
    assert widget_int2.dataValue() == 42

    widget_float2 = dclswidget.widgets()["float2"]
    assert widget_float2.text() == "4.2"
    assert widget_float2.dataValue() == 4.2

    widget_str2 = dclswidget.widgets()["str2"]
    assert widget_str2.text() == "foo"

    widget_Tuple3 = dclswidget.widgets()["Tuple3"]
    assert widget_Tuple3.widgets()[0].isChecked()
    assert widget_Tuple3.widgets()[1].text() == "1"
    assert widget_Tuple3.widgets()[1].dataValue() == 1

    widget_Tuple4 = dclswidget.widgets()["Tuple4"]
    assert not widget_Tuple4.widgets()[0].isChecked()
    assert widget_Tuple4.widgets()[1].widgets()[0].text() == "2"
    assert widget_Tuple4.widgets()[1].widgets()[0].dataValue() == 2


def test_DataclassWidget_dataChanged(qtbot, dclswidget):
    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["bool1"].setChecked(True)

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["int1"].setText("42")

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["float1"].setText("4.2")

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["str1"].setText("foo")

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["Tuple1"].widgets()[0].setChecked(True)

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["Tuple1"].widgets()[1].setText("42")

    with qtbot.waitSignal(dclswidget.dataChanged, raising=True):
        dclswidget.widgets()["Tuple2"].widgets()[1].widgets()[0].setText("42")


def test_DataclassWidget_currentData(qtbot, dclswidget):
    dclstype = dclswidget.dataclassType()

    assert dclswidget.currentData() == dclstype(bool1=False,
                                                int1=int(0),
                                                float1=float(0),
                                                str1="",
                                                Tuple1=(False, 0),
                                                Tuple2=(False, (0,)))


def test_DataclassWidget_applyData(qtbot, dclswidget):
    dc = dclswidget.dataclassType()(bool1=True,
                                    int1=42,
                                    float1=4.2,
                                    str1="foo",
                                    Tuple1=(False, 0),
                                    Tuple2=(False, (0,)))

    dclswidget.applyData(dc)
    assert dclswidget.currentData() == dc
