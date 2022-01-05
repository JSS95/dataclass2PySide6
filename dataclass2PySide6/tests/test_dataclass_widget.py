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

@pytest.fixture
def nested_dcw(qtbot):

    @dataclasses.dataclass
    class DataClass1:
        z: int

    @dataclasses.dataclass
    class DataClass2:
        x: int
        y: DataClass1

    @dataclasses.dataclass
    class DataClass3:
        a: bool
        b: DataClass2

    widget = DataclassWidget.fromDataclass(DataClass3)
    return widget


def test_DataclassWidget_construction(qtbot, dclswidget):

    widget_bool1 = dclswidget.widgets()["bool1"]
    assert not widget_bool1.isChecked()
    assert widget_bool1.text() == "bool1"

    widget_int1 = dclswidget.widgets()["int1"]
    assert widget_int1.placeholderText() == "int1"
    assert widget_int1.text() == ""

    widget_float1 = dclswidget.widgets()["float1"]
    assert widget_float1.placeholderText() == "float1"
    assert widget_float1.text() == ""

    widget_str1 = dclswidget.widgets()["str1"]
    assert widget_str1.placeholderText() == "str1"
    assert widget_str1.text() == ""

    widget_Tuple1 = dclswidget.widgets()["Tuple1"]
    assert widget_Tuple1.title() == "Tuple1"
    assert not widget_Tuple1.widgets()[0].isChecked()
    assert widget_Tuple1.widgets()[1].text() == ""

    widget_Tuple2 = dclswidget.widgets()["Tuple2"]
    assert not widget_Tuple2.widgets()[0].isChecked()
    assert widget_Tuple2.widgets()[1].widgets()[0].text() == ""

    widget_bool2 = dclswidget.widgets()["bool2"]
    assert widget_bool2.isChecked()

    widget_bool3 = dclswidget.widgets()["bool3"]
    assert not widget_bool3.isChecked()

    widget_int2 = dclswidget.widgets()["int2"]
    assert widget_int2.text() == "42"

    widget_float2 = dclswidget.widgets()["float2"]
    assert widget_float2.text() == "4.2"

    widget_str2 = dclswidget.widgets()["str2"]
    assert widget_str2.text() == "foo"

    widget_Tuple3 = dclswidget.widgets()["Tuple3"]
    assert widget_Tuple3.widgets()[0].isChecked()
    assert widget_Tuple3.widgets()[1].text() == "1"

    widget_Tuple4 = dclswidget.widgets()["Tuple4"]
    assert not widget_Tuple4.widgets()[0].isChecked()
    assert widget_Tuple4.widgets()[1].widgets()[0].text() == "2"


def test_nested_DataclassWidget_construction(qtbot, nested_dcw):
    widget_dcls2 = nested_dcw.widgets()["b"]
    widget_dcls1 = widget_dcls2.widgets()["y"]

    assert widget_dcls1.dataName() == "y"
    assert widget_dcls2.dataName() == "b"


def test_DataclassWidget_dataValueChanged(qtbot, dclswidget):
    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["bool1"].setChecked(True)

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["int1"].setText("42")

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["float1"].setText("4.2")

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["str1"].setText("foo")

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["Tuple1"].widgets()[0].setChecked(True)

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["Tuple1"].widgets()[1].setText("42")

    with qtbot.waitSignal(dclswidget.dataValueChanged, raising=True):
        dclswidget.widgets()["Tuple2"].widgets()[1].widgets()[0].setText("42")


def test_nested_DataclassWidget_dataValueChanged(qtbot, nested_dcw):
    widget_dcls2 = nested_dcw.widgets()["b"]
    widget_dcls1 = widget_dcls2.widgets()["y"]

    with qtbot.waitSignal(nested_dcw.dataValueChanged, raising=True):
        widget_dcls1.widgets()["z"].setText("10")

    with qtbot.waitSignal(nested_dcw.dataValueChanged, raising=True):
        widget_dcls2.widgets()["x"].setText("10")

    with qtbot.waitSignal(nested_dcw.dataValueChanged, raising=True):
        nested_dcw.widgets()["a"].setChecked(True)


def test_DataclassWidget_dataValue(qtbot, dclswidget):
    dclstype = dclswidget.dataclassType()

    assert dclswidget.dataValue() == dclstype(bool1=False,
                                              int1=int(0),
                                              float1=float(0),
                                              str1="",
                                              Tuple1=(False, 0),
                                              Tuple2=(False, (0,)))


def test_nested_DataclassWidget_dataValue(qtbot, nested_dcw):
    dcls3 = nested_dcw.dataclassType()
    widget_dcls2 = nested_dcw.widgets()["b"]
    dcls2 = widget_dcls2.dataclassType()
    widget_dcls1 = widget_dcls2.widgets()["y"]
    dcls1 = widget_dcls1.dataclassType()

    assert nested_dcw.dataValue() == dcls3(a=False, b=dcls2(x=0, y=dcls1(z=0)))


def test_DataclassWidget_setDataValue(qtbot, dclswidget):
    dc = dclswidget.dataclassType()(bool1=True,
                                    int1=42,
                                    float1=4.2,
                                    str1="foo",
                                    Tuple1=(False, 0),
                                    Tuple2=(False, (0,)))

    dclswidget.setDataValue(dc)
    assert dclswidget.dataValue() == dc


def test_nested_DataclassWidget_setDataValue(qtbot, nested_dcw):
    dcls3 = nested_dcw.dataclassType()
    widget_dcls2 = nested_dcw.widgets()["b"]
    dcls2 = widget_dcls2.dataclassType()
    widget_dcls1 = widget_dcls2.widgets()["y"]
    dcls1 = widget_dcls1.dataclassType()

    dc = dcls3(a=True, b=dcls2(x=-1, y=dcls1(z=100)))
    nested_dcw.setDataValue(dc)
    assert nested_dcw.dataValue() == dc
