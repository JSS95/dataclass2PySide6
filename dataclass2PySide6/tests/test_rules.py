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

    widget2 = bool2QCheckBox(y)
    assert widget2.isCheckable()
    assert widget2.isChecked()

    widget2 = bool2QCheckBox(z)
    assert widget2.isCheckable()
    assert not widget2.isChecked()
