import dataclasses
from PySide6.QtWidgets import QCheckBox, QLineEdit
from dataclass2PySide6 import DataclassWidget, IntLineEdit, FloatLineEdit


def test_DataclassWidget_construction(qtbot):
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

    widget_a = widget.widgets()["a"]
    assert widget_a.isCheckable()
    assert not widget_a.isChecked()
    assert widget_a.text() == "a"
    assert isinstance(widget_a, QCheckBox)

    widget_b = widget.widgets()["b"]
    assert widget_b.placeholderText() == "b"
    assert widget_b.text() == ""
    assert isinstance(widget_b, IntLineEdit)

    widget_c = widget.widgets()["c"]
    assert widget_c.placeholderText() == "c"
    assert widget_c.text() == ""
    assert isinstance(widget_c, FloatLineEdit)

    widget_d = widget.widgets()["d"]
    assert widget_d.placeholderText() == "d"
    assert widget_d.text() == ""
    assert isinstance(widget_d, QLineEdit)

    widget_e = widget.widgets()["e"]
    assert widget_e.isChecked()

    widget_f = widget.widgets()["f"]
    assert not widget_f.isChecked()

    widget_g = widget.widgets()["g"]
    assert widget_g.text() == "42"

    widget_h = widget.widgets()["h"]
    assert widget_h.text() == "4.2"

    widget_i = widget.widgets()["i"]
    assert widget_i.text() == "foo"
