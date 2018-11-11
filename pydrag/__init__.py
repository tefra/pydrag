from abc import ABCMeta
from typing import Dict, TypeVar

import cattr
from attr import attrib
from cattr import unstructure, structure
from dotenv import load_dotenv
from requests import Response

load_dotenv()

T = TypeVar("T", bound="BaseModel")


def mattrib(name, **kwargs):
    metadata = kwargs.get("metadata", {})
    metadata.update(dict(name=name))
    kwargs.update(dict(metadata=metadata))
    return attrib(**kwargs)


class BaseModel(metaclass=ABCMeta):

    namespace: str = attrib(init=False)
    method: str = attrib(init=False)
    params: dict = attrib(init=False)
    response: Response = attrib(init=False)

    def to_dict(self: T) -> Dict:
        return unstructure(self)

    def get_fields(self):
        return self.__class__.__attrs_attrs__

    @classmethod
    def from_dict(cls: T, data: dict) -> T:
        return structure(data, cls)


def structure_attrs_fromdict(obj, cl):
    conv_obj = dict()
    dispatch = cattr.global_converter._structure_func.dispatch
    for a in cl.__attrs_attrs__:
        type_ = a.type
        if type_ is None:
            continue
        name = a.name
        meta_name = a.metadata.get("name")

        if name in obj:
            value = obj[name]
        elif meta_name and meta_name in obj:
            value = obj[meta_name]
        else:
            continue

        conv_obj[name] = dispatch(type_)(value, type_)

    return cl(**conv_obj)


def unstructure_attrs_asdict(obj):
    attrs = obj.__class__.__attrs_attrs__
    dispatch = cattr.global_converter._unstructure_func.dispatch
    rv = cattr.global_converter._dict_factory()
    for a in attrs:
        name = a.name
        v = getattr(obj, name)
        name = a.metadata.get("name", name)

        if v is None:
            continue

        rv[name] = dispatch(v.__class__)(v)
    return rv


cattr.register_structure_hook(BaseModel, structure_attrs_fromdict)
cattr.register_unstructure_hook(BaseModel, unstructure_attrs_asdict)
