from attr import dataclass

from pydrag.core import BaseModel


@dataclass
class Attributes(BaseModel):
    timestamp: int = None
    rank: str = None
    date: str = None
    ignored: int = None
    position: int = None
    accepted: int = None


@dataclass
class RootAttributes(BaseModel):
    tag: str = None
    page: int = None
    user: str = None
    country: str = None
    total: int = None
    album: str = None
    artist: str = None
    limit: int = None
    track: str = None
    total_pages: int = None
    to_date: str = None
    from_date: str = None
    offset: int = None
    timestamp: int = None
    rank: str = None
    date: str = None
    ignored: int = None
    position: int = None
    accepted: int = None


@dataclass
class AttrModel(BaseModel):
    attr: RootAttributes = None


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
class Links(BaseModel):
    link: Link


@dataclass
class Wiki(BaseModel):
    content: str = None
    summary: str = None
    published: str = None
    links: Links = None
