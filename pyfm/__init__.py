from abc import ABCMeta
from json import dumps, loads
from typing import Dict, TypeVar

import cattr
from attr import evolve
from cattr import unstructure, structure
from requests import Response

T = TypeVar("T", bound="BaseModel")


class BaseModel(metaclass=ABCMeta):
    @property
    def response(self) -> Response:
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def to_dict(self: T) -> Dict:
        return unstructure(self)

    def to_json(self: T, indent=4, **kwargs) -> str:
        return dumps(unstructure(self), indent=indent, **kwargs)

    def copy(self: T, **kwargs) -> T:
        return evolve(self, **kwargs)

    @classmethod
    def from_json(cls: T, stream) -> T:
        stream = stream.read() if hasattr(stream, "read") else stream
        data = loads(stream)

        if isinstance(data, list) and len(data) == 1:
            data = data[0]

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls: T, data: dict) -> T:
        return structure(data, cls)


def structure_attrs_fromdict(obj, cl):
    # type: (Mapping, Type) -> Any
    """Instantiate an attrs class from a mapping (dict) that ignores unknown
    fields `cattr issue <https://github.com/Tinche/cattrs/issues/35>`_"""
    # For public use.

    # conv_obj = obj.copy()  # Dict of converted parameters.
    conv_obj = dict()  # Start fresh

    # dispatch = self._structure_func.dispatch
    dispatch = cattr.global_converter._structure_func.dispatch  # Ugly I know
    for a in cl.__attrs_attrs__:
        # We detect the type by metadata.
        type_ = a.type
        if type_ is None:
            # No type.
            continue
        name = a.name

        if name in obj:
            value = obj[name]
        elif "#" + name in obj:
            value = obj["#" + name]
        elif "@" + name in obj:
            value = obj["@" + name]
        elif name == "user" and "for" in obj:
            value = obj["for"]
        elif name == "from_date" and "from" in obj:
            value = obj["from"]
        else:
            continue

        conv_obj[name] = dispatch(type_)(value, type_)

    return cl(**conv_obj)


def unstructure_attrs_asdict(obj):
    """Our version of `attrs.asdict`, so we can call back to us."""
    attrs = obj.__class__.__attrs_attrs__
    dispatch = cattr.global_converter._unstructure_func.dispatch
    rv = cattr.global_converter._dict_factory()
    for a in attrs:
        name = a.name
        v = getattr(obj, name)

        if name == "attr":
            name = "@attr"
        elif name == "text":
            name = "#text"

        if v is None:
            continue

        rv[name] = dispatch(v.__class__)(v)
    return rv


cattr.register_structure_hook(BaseModel, structure_attrs_fromdict)
cattr.register_unstructure_hook(BaseModel, unstructure_attrs_asdict)
