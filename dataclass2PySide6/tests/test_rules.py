import dataclasses
from dataclass2PySide6 import bool2QCheckBox, int2LineEdit


def test_bool2QCheckBox(qtbot):

    @dataclasses.dataclass
    class BoolDataClass:
        x: bool
        y: bool = True
        z: bool = False

    x, y, z = dataclasses.fields(BoolDataClass)

    widget1 = bool2QCheckBox(x)
    assert widget1.isCheckable()
    assert not widget1.isChecked()
    assert widget1.text() == "x"

    widget2 = bool2QCheckBox(y)
    assert widget2.isCheckable()
    assert widget2.isChecked()
    assert widget2.text() == "y"

    widget3 = bool2QCheckBox(z)
    assert widget3.isCheckable()
    assert not widget3.isChecked()
    assert widget3.text() == "z"


def test_int2LineEdit(qtbot):

    @dataclasses.dataclass
    class IntDataClass:
        x: int
        y: int = 1

    x, y = dataclasses.fields(IntDataClass)

    widget1 = int2LineEdit(x)
    assert widget1.placeholderText() == "x"
    assert widget1.text() == ""

    widget2 = int2LineEdit(y)
    assert widget2.placeholderText() == "y"
    assert widget2.text() == "1"