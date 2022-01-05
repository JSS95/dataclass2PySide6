import dataclasses
import pytest
from PySide6.QtWidgets import QCheckBox, QLineEdit
from dataclass2PySide6 import DataclassWidget, IntLineEdit, FloatLineEdit


@pytest.fixture
def dclswidget(qtbot):

    @dataclasses.dataclass
    class DataClass:
        a: bool
        b: int
        c: float
        d: str
        e: bool = True
        f: bool = False
        g: int = 42
        h: float = 4.2
        i: str = "foo"

    widget = DataclassWidget.fromDataclass(DataClass)
    return widget


def test_DataclassWidget_construction(qtbot, dclswidget):

    widget_a = dclswidget.widgets()["a"]
    assert widget_a.isCheckable()
    assert not widget_a.isChecked()
    assert widget_a.text() == "a"
    assert isinstance(widget_a, QCheckBox)

    widget_b = dclswidget.widgets()["b"]
    assert widget_b.placeholderText() == "b"
    assert widget_b.text() == ""
    assert isinstance(widget_b, IntLineEdit)

    widget_c = dclswidget.widgets()["c"]
    assert widget_c.placeholderText() == "c"
    assert widget_c.text() == ""
    assert isinstance(widget_c, FloatLineEdit)

    widget_d = dclswidget.widgets()["d"]
    assert widget_d.placeholderText() == "d"
    assert widget_d.text() == ""
    assert isinstance(widget_d, QLineEdit)

    widget_e = dclswidget.widgets()["e"]
    assert widget_e.isChecked()

    widget_f = dclswidget.widgets()["f"]
    assert not widget_f.isChecked()

    widget_g = dclswidget.widgets()["g"]
    assert widget_g.text() == "42"

    widget_h = dclswidget.widgets()["h"]
    assert widget_h.text() == "4.2"

    widget_i = dclswidget.widgets()["i"]
    assert widget_i.text() == "foo"
