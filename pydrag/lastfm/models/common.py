from math import ceil
from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.mixins import PagerMixin


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
    limit: int = mattrib("perPage", default=None)
    track: str = None
    total_pages: int = mattrib("totalPages", default=None)
    accepted: int = None
    ignored: int = None
    track_corrected: int = mattrib("trackcorrected", default=None)
    artist_corrected: int = mattrib("artistcorrected", default=None)
    to_date: str = mattrib("to", default=None)
    for_user: str = mattrib("for", default=None)
    from_date: str = mattrib("from", default=None)


@attrs(auto_attribs=True)
class AttrModel(BaseModel, PagerMixin):
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Image(BaseModel):
    size: str
    text: str = mattrib("#text")


@attrs(auto_attribs=True)
class Date(BaseModel):
    timestamp: int = mattrib("unixtime")
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
    tag_count: int = mattrib("tagcount", default=None)
    listeners: int = None
    playcount: int = None
    streamable: str = None
    image: List[Image] = None
    match: str = None
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class Artists(BaseModel):
    artist: List[Artist]


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
    image: List[Image] = None
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class Albums(BaseModel):
    album: List[Album]


@attrs(auto_attribs=True)
class Chart(BaseModel):
    text: str = mattrib("#text")
    from_date: str = mattrib("from")
    to_date: str = mattrib("to")


@attrs(auto_attribs=True)
class Charts(BaseModel):
    chart: List[Chart]


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
class TagInfo(BaseModel):
    name: str
    reach: int
    url: str = None
    taggings: int = None
    count: int = None
    total: int = None
    wiki: Wiki = None


@attrs(auto_attribs=True)
class TagInfos(BaseModel):
    tag: List[TagInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tag(BaseModel):
    name: str
    url: str
    count: int = None


@attrs(auto_attribs=True)
class Tags(BaseModel):
    tag: List[Tag]


@attrs(auto_attribs=True)
class Query(BaseModel):
    role: str
    page: int = mattrib("startPage")
    text: str = mattrib("#text")
    search_terms: str = mattrib("searchTerms", default=None)


@attrs(auto_attribs=True)
class OpenSearch(AttrModel):
    query: Query = mattrib("opensearch:Query")
    limit: int = mattrib("opensearch:itemsPerPage")
    offset: int = mattrib("opensearch:startIndex")
    total: int = mattrib("opensearch:totalResults")

    def get_page(self):
        return self.query.page

    def get_limit(self):
        return self.limit

    def get_total(self):
        return self.total

    def get_total_pages(self):
        return ceil(self.total / self.limit)
