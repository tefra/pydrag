from typing import List, Optional

from attr import dataclass

from pydrag.core import BaseModel


@dataclass
class Attributes(BaseModel):
    tag: Optional[str] = None
    page: Optional[int] = None
    user: Optional[str] = None
    country: Optional[str] = None
    total: Optional[int] = None
    album: Optional[str] = None
    artist: Optional[str] = None
    limit: Optional[int] = None
    track: Optional[str] = None
    total_pages: Optional[int] = None
    to_date: Optional[str] = None
    from_date: Optional[str] = None
    offset: Optional[int] = None
    timestamp: Optional[int] = None
    rank: Optional[int] = None
    date: Optional[str] = None
    ignored: Optional[int] = None
    position: Optional[int] = None
    accepted: Optional[int] = None


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
        return super().from_dict(data)
