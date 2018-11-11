from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib


@attrs(auto_attribs=True)
class Attributes(BaseModel):
    tag: str = None
    uts: str = None
    rank: str = None
    date: str = None
    page: int = None
    user: str = None
    index: int = None
    country: str = None
    total: int = None
    album: str = None
    offset: int = None
    artist: str = None
    position: int = None
    num_res: int = None
    perPage: int = None
    track: str = None
    totalPages: int = None
    accepted: int = None
    ignored: int = None
    trackcorrected: int = None
    artistcorrected: int = None
    to_date: str = mattrib("to", default=None)
    for_user: str = mattrib("for", default=None)
    from_date: str = mattrib("from", default=None)


@attrs(auto_attribs=True)
class Image(BaseModel):
    size: str
    text: str = mattrib("#text")


@attrs(auto_attribs=True)
class Date(BaseModel):
    unixtime: int
    text: str = mattrib("#text")


@attrs(auto_attribs=True)
class DateUTS(BaseModel):
    uts: str
    text: str = mattrib("#text")


@attrs(auto_attribs=True)
class Artist(BaseModel):
    mbid: str = None
    name: str = None
    text: str = mattrib("#text", default=None)
    url: str = None
    tagcount: int = None
    listeners: int = None
    playcount: int = None
    streamable: str = None
    image: List[Image] = None
    match: str = None
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class Track(BaseModel):
    name: str
    url: str
    artist: Artist
    mbid: str = None
    image: List[Image] = None
    playcount: int = None
    listeners: int = None
    streamable: str = None  # super buggy
    duration: str = None
    match: float = None
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class Tracks(BaseModel):
    track: List[Track]


@attrs(auto_attribs=True)
class TracksAttr(Tracks):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TrackSimpleArtist(Track):
    artist: str = None


@attrs(auto_attribs=True)
class Album(BaseModel):
    mbid: str = None
    text: str = mattrib("#text", default=None)
    name: str = None
    title: str = None
    playcount: int = None
    url: str = None
    artist: Artist = None
    attr: Attributes = mattrib("@attr", default=None)
    image: List[Image] = None


@attrs(auto_attribs=True)
class Chart(BaseModel):
    text: str = mattrib("#text")
    from_date: str = mattrib("from")
    to_date: str = mattrib("to")


@attrs(auto_attribs=True)
class Link(BaseModel):
    href: str
    rel: str
    text: str = mattrib("#text")


@attrs(auto_attribs=True)
class Links(BaseModel):
    link: Link


@attrs(auto_attribs=True)
class Wiki(BaseModel):
    content: str = None
    summary: str = None
    published: str = None
    links: Links = None


@attrs(auto_attribs=True)
class Tag(BaseModel):
    name: str
    url: str
    count: int = None


@attrs(auto_attribs=True)
class Tags(BaseModel):
    tag: List[Tag]


@attrs(auto_attribs=True)
class TagsAttr(Tags):
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Query(BaseModel):
    role: str
    startPage: int
    text: str = mattrib("#text")
    searchTerms: str = None


@attrs(auto_attribs=True)
class OpenSearch(BaseModel):
    query: Query = mattrib("opensearch:Query")
    itemsPerPage: int = mattrib("opensearch:itemsPerPage")
    startIndex: int = mattrib("opensearch:startIndex")
    totalResults: int = mattrib("opensearch:totalResults")
    attr: Attributes = mattrib("@attr")
