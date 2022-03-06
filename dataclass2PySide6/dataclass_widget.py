import dataclasses
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QGroupBox, QVBoxLayout, QStackedWidget,
    QTabWidget, QSizePolicy)
from typing import Dict, Optional, get_type_hints, Any, Type

from .datawidgets import type2Widget
from .typing import DataclassProtocol


__all__ = [
    'DataclassWidget',
    'StackedDataclassWidget',
    'TabDataclassWidget',
]


@dataclasses.dataclass
class _DefaultDataclass:
    """
    Default empty dataclass for uninitialized :class:`DataclassWidget`.
    """
    pass


class DataclassWidget(QGroupBox):
    """
    Widget for a dataclass type. Subwidgets represent the fields of the
    dataclass.

    Standard way to construct this widget is passing the dataclass type
    to :meth:`fromDataclass` class method. The class searches for
    ``Qt_typehint`` metadata from each field to determine the subwidget
    type. If ``Qt_typehint`` does not exist, type of the field is used
    as a fallback. Dataclass type used to construct the instance can be
    retrieved by :meth:`dataclasType`.

    :meth:`dataValue` constructs and returns the dataclass instance from
    the current data of the widgets. If field of :meth:`dataclasType`
    has ``fromQt_converter`` metadata, it is used to convert the widget
    data to field value.

    :meth:`setDataValue` updates the current states of the widgets with
    dataclass instance. If field of :meth:`dataclasType` has
    ``toQt_converter`` metadata, it is used to convert the fied value
    to widget data.

    Whenever the data from subwidget is changed and values are all set,
    :attr:`dataValueChanged` emits the entire new dataclass instance.

    Subclass may redefine :meth:`field2Widget` method to change how the
    subwidgets are constructed by the field. Every subwidget must have
    ``dataValue()`` method which returns the current value,
    ``dataValueChanged`` signal which emits the changed value,
    and ``setDataValue()`` slot which updates the current value.

    Examples
    ========

    Nested dataclasses are recursively constructed.

    >>> from dataclasses import dataclass, field
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from typing import Union
    >>> from dataclass2PySide6 import DataclassWidget
    >>> asUpper = lambda string: string.upper()
    >>> @dataclass
    ... class DataClass1:
    ...     a: Union[int, str] = field(metadata=dict(Qt_typehint=str))
    ...     b: str = field(metadata=dict(fromQt_converter=asUpper))
    >>> @dataclass
    ... class DataClass2:
    ...     x: int
    ...     y: DataClass1
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = DataclassWidget.fromDataclass(DataClass2)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP
    """

    dataValueChanged = Signal(object)

    @classmethod
    def fromDataclass(cls, datacls: Type[DataclassProtocol]) \
                     -> 'DataclassWidget':
        """
        Construct the widget using the fields from the dataclass.

        If the field has ``Qt_typehint`` metadata, use its value to
        construct the widget. If not, use `Field.type` as a fallback.

        """
        obj = cls()
        obj._dataclass_type = datacls
        fields = dataclasses.fields(datacls)
        annots = get_type_hints(datacls.__init__)

        widgets = {}
        for f in fields:
            if 'Qt_typehint' in f.metadata:
                typehint = f.metadata['Qt_typehint']
            else:
                typehint = annots[f.name]
            w = obj.field2Widget(typehint, f)
            widgets[f.name] = w
        obj._widgets = widgets
        obj.initWidgets()
        obj.initUI()
        return obj

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataclass_type = _DefaultDataclass
        self._widgets = {}

    @classmethod
    def field2Widget(cls, typehint: Any, field: dataclasses.Field) -> QWidget:
        """Return a widget for *field*."""
        if dataclasses.is_dataclass(typehint):
            widget = cls.fromDataclass(typehint)
        else:
            widget = type2Widget(typehint)
        widget.setDataName(field.name)

        default = field.default
        if default != dataclasses.MISSING:
            widget.setDataValue(default)

        return widget

    def dataclassType(self) -> Type[DataclassProtocol]:
        """Dataclass type which is used to construct *self*."""
        return self._dataclass_type

    def dataName(self) -> str:
        return self.title()

    def setDataName(self, name: str):
        self.setTitle(name)

    def widgets(self) -> Dict[str, QWidget]:
        """
        Sub-widgets which represent the fields of :meth:`dataclassType`.
        """
        return self._widgets

    def initWidgets(self):
        """Initialize the widgets in :meth:`widgets`."""
        for widget in self.widgets().values():
            widget.dataValueChanged.connect(self.emitDataValueChanged)

    def initUI(self):
        """Initialize the UI with :meth:`widgets`."""
        layout = QVBoxLayout()
        for widget in self.widgets().values():
            layout.addWidget(widget)
        self.setLayout(layout)

    def emitDataValueChanged(self):
        try:
            val = self.dataValue()
            self.dataValueChanged.emit(val)
        except (TypeError, ValueError):
            pass

    def dataValue(self) -> DataclassProtocol:
        """
        Return the current state of widgets as dataclass instance.

        Fields of :meth:`dataclassType` can have ``fromQt_converter``
        metadata whose value is a unary function which takes the data
        value of subwidget. It is used to construct the value for the
        field.

        """
        widgets = self.widgets()
        dcls = self.dataclassType()
        args = {}
        for f in dataclasses.fields(dcls):
            val = widgets[f.name].dataValue()
            converter = f.metadata.get('fromQt_converter', None)
            if converter is not None:
                val = converter(val)
            args[f.name] = val
        data = dcls(**args)
        return data

    def setDataValue(self, data: DataclassProtocol):
        """
        Apply the dataclass instance to data widgets states.

        Fields of :meth:`dataclassType` can have ``toQt_converter``
        metadata whose value is a unary function which takes the field
        value. Its return value is updated to the subwidget.

        """
        widgets = self.widgets()
        dcls = self.dataclassType()

        for f in dataclasses.fields(dcls):
            val = getattr(data, f.name)
            converter = f.metadata.get('toQt_converter', None)
            if converter is not None:
                val = converter(val)

            w = widgets[f.name]
            w.setDataValue(val)


class StackedDataclassWidget(QStackedWidget):
    """
    Stacked dataclass widgets.

    Use :meth:`addDataclass` to construct and add the widget for the
    dataclass. Use :meth:`indexOfDataclass` to get the index of the
    widget for giten dataclass.

    If data value of any dataclass widget is changed,
    :attr:`dataValueChanged` signal emits the new value.

    Examples
    ========

    >>> from dataclasses import dataclass
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import StackedDataclassWidget
    >>> @dataclass
    ... class DataClass1:
    ...     a: int
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = StackedDataclassWidget()
    ...     widget.addDataclass(DataClass1)
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """

    dataValueChanged = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._dataclasses: Dict[Type[DataclassProtocol], int] = {}

    def addWidget(self, w: QWidget):
        # force size policy to make ignore the size of hidden widget
        w.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Ignored
        )
        super().addWidget(w)

    def setCurrentIndex(self, index: int):
        old_widget = self.currentWidget()
        if old_widget is not None:
            old_widget.setSizePolicy(
                QSizePolicy.Ignored,
                QSizePolicy.Ignored
            )
        new_widget = self.widget(index)
        if new_widget is not None:
            new_widget.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred
            )
            new_widget.adjustSize()
        super().setCurrentIndex(index)
        self.adjustSize()

    def setCurrentWidget(self, w: QWidget):
        old_widget = self.currentWidget()
        if old_widget is not None:
            old_widget.setSizePolicy(
                QSizePolicy.Ignored,
                QSizePolicy.Ignored
            )
        if w is not None:
            w.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred
            )
            w.adjustSize()
        super().setCurrentWidget(w)
        self.adjustSize()

    def addDataclass(self,
                     dcls: Type[DataclassProtocol],
                     name: Optional[str] = None):
        """Construct and add the :class:`DataclassWidget`"""
        if name is None:
            name = dcls.__name__
        widget = DataclassWidget.fromDataclass(dcls)
        widget.setDataName(name)
        self.addWidget(widget)
        self._dataclasses[dcls] = self.indexOf(widget)
        widget.dataValueChanged.connect(self.emitDataValueChanged)

    def indexOfDataclass(self, dcls: Type[DataclassProtocol]) -> int:
        """Returns the index of the widget for *dcls*."""
        return self._dataclasses.get(dcls, -1)

    def emitDataValueChanged(self):
        try:
            val = self.currentWidget().dataValue()
            self.dataValueChanged.emit(val)
        except (TypeError, ValueError):
            pass


class TabDataclassWidget(QTabWidget):
    """
    Tabbed dataclass widgets.

    Use :meth:`addDataclass` to construct and add the widget for the
    dataclass. Use :meth:`indexOfDataclass` to get the index of the widget for
    giten dataclass.

    If data value of any dataclass widget is changed,
    :attr:`dataValueChanged` signal emits the new value.

    Examples
    ========

    >>> from dataclasses import dataclass
    >>> from PySide6.QtWidgets import QApplication
    >>> import sys
    >>> from dataclass2PySide6 import TabDataclassWidget
    >>> @dataclass
    ... class DataClass1:
    ...     a: int
    >>> @dataclass
    ... class DataClass2:
    ...     b: int
    >>> def runGUI():
    ...     app = QApplication(sys.argv)
    ...     widget = TabDataclassWidget()
    ...     widget.addDataclass(DataClass1, 'data1')
    ...     widget.addDataclass(DataClass2, 'data2')
    ...     widget.show()
    ...     app.exec()
    ...     app.quit()
    >>> runGUI() # doctest: +SKIP

    """
    dataValueChanged = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._dataclasses: Dict[Type[DataclassProtocol], int] = {}

    def addTab(self, widget: QWidget, *args):
        # force size policy to make ignore the size of hidden widget
        widget.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Ignored
        )
        super().addTab(widget, *args)

    def setCurrentIndex(self, index: int):
        old_widget = self.currentWidget()
        if old_widget is not None:
            old_widget.setSizePolicy(
                QSizePolicy.Ignored,
                QSizePolicy.Ignored
            )
        new_widget = self.widget(index)
        if new_widget is not None:
            new_widget.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred
            )
            new_widget.adjustSize()
        super().setCurrentIndex(index)
        self.adjustSize()

    def setCurrentWidget(self, w: QWidget):
        old_widget = self.currentWidget()
        if old_widget is not None:
            old_widget.setSizePolicy(
                QSizePolicy.Ignored,
                QSizePolicy.Ignored
            )
        if w is not None:
            w.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Preferred
            )
            w.adjustSize()
        super().setCurrentWidget(w)
        self.adjustSize()

    def addDataclass(self, dcls: Type[DataclassProtocol], label: str):
        """Construct and add the :class:`DataclassWidget`"""
        widget = DataclassWidget.fromDataclass(dcls)
        self.addTab(widget, label)
        self._dataclasses[dcls] = self.indexOf(widget)
        widget.dataValueChanged.connect(self.emitDataValueChanged)

    def indexOfDataclass(self, dcls: Type[DataclassProtocol]) -> int:
        """Returns the index of the widget for *dcls*."""
        return self._dataclasses.get(dcls, -1)

    def emitDataValueChanged(self):
        try:
            val = self.currentWidget().dataValue()
            self.dataValueChanged.emit(val)
        except (TypeError, ValueError):
            pass
