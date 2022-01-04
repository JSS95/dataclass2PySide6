import dataclasses
from dataclass2PySide6 import bool2QCheckBox


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
