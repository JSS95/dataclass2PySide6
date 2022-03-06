from typing import Protocol, Dict, Optional, Callable


__all__ = [
    'DataclassProtocol',
]


class DataclassProtocol(Protocol):
    """Type annotation for dataclass type object"""
    # https://stackoverflow.com/a/70114354/11501976
    __dataclass_fields__: Dict
    __dataclass_params__: Dict
    __post_init__: Optional[Callable]
