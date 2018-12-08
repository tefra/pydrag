from collections import UserList
from typing import Dict, List, Optional, Sequence, Type, TypeVar

from attr import asdict, attrib, dataclass, fields

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    params: Optional[dict] = attrib(init=False)

    def to_dict(self: "BaseModel") -> Dict:
        """
        Convert our object to a traditional dictionary. Filter out None values
        and dictionary values. The last one is like a validation for the unit
        tests in case we forgot to properly deserialize an dict to an object.

        :rtype: Dict
        """
        return asdict(
            self, filter=lambda f, v: v is not None and type(v) != dict
        )

    @classmethod
    def from_dict(cls: Type, data: dict) -> "BaseModel":
        for f in fields(cls):
            if f.name not in data or data[f.name] is None:
                continue

            if f.type == str or f.type == Optional[str]:
                data[f.name] = str(data[f.name])
            elif f.type == int or f.type == Optional[int]:
                data[f.name] = int(data[f.name])
            elif f.type == float or f.type == Optional[float]:
                data[f.name] = float(data[f.name])

        return cls(**data)


@dataclass(cmp=False)
class ListModel(UserList, Sequence[T]):
    data: List[T] = []

    def to_dict(self) -> Dict:
        return dict(data=[item.to_dict() for item in self])


@dataclass
class RawResponse(BaseModel):
    data: Optional[dict] = None

    def to_dict(self):
        return self.data

    @classmethod
    def from_dict(cls, data):
        return cls(data)


@dataclass
class Attributes(BaseModel):
    timestamp: Optional[int] = None
    rank: Optional[int] = None
    date: Optional[str] = None
    position: Optional[int] = None


@dataclass
class Image(BaseModel):
    size: str
    text: str


@dataclass
class Date(BaseModel):
    timestamp: int
    text: str


@dataclass
class Chart(BaseModel):
    text: str
    from_date: str
    to_date: str


@dataclass
class Link(BaseModel):
    href: str
    rel: str
    text: str


@dataclass
class Wiki(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    published: Optional[str] = None
    links: Optional[List[Link]] = None

    @classmethod
    def from_dict(cls, data: dict):
        if "links" in data:
            if isinstance(data["links"]["link"], dict):
                data["links"]["link"] = [data["links"]["link"]]

            data["links"] = list(map(Link.from_dict, data["links"]["link"]))
        return super(Wiki, cls).from_dict(data)
