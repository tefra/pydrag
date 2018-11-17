from math import ceil
from typing import List, Optional

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.mixins import PagerMixin


@dataclass
class Attributes(BaseModel):
    tag: str = None
    timestamp: int = None
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
    limit: int = None
    track: str = None
    total_pages: int = None
    accepted: int = None
    ignored: int = None
    track_corrected: int = None
    artist_corrected: int = None
    to_date: str = None
    from_date: str = None


@dataclass
class AttrModel(BaseModel, PagerMixin):
    attr: Attributes


@dataclass
class Image(BaseModel):
    size: str
    text: str


@dataclass
class Date(BaseModel):
    timestamp: int
    text: str


@dataclass
class SimpleArtist(BaseModel):
    mbid: str = None
    name: str = None
    url: str = None
    text: str = None


@dataclass
class Artist(BaseModel):
    mbid: str = None
    name: str = None
    url: str = None
    tag_count: int = None
    listeners: int = None
    playcount: int = None
    streamable: str = None
    image: List[Image] = None
    match: str = None
    attr: Attributes = None


@dataclass
class Artists(BaseModel):
    artist: List[Artist]


@dataclass
class ArtistList(Artists, AttrModel):
    pass


@dataclass
class Track(BaseModel):
    name: str
    url: str
    artist: SimpleArtist
    mbid: str = None
    image: List[Image] = None
    playcount: int = None
    listeners: int = None
    streamable: str = None
    duration: str = None
    match: Optional[float] = None
    attr: Attributes = None


@dataclass
class Tracks(BaseModel):
    track: List[Track]


@dataclass
class TrackList(Tracks, AttrModel):
    pass


@dataclass
class TrackSimpleArtist(Track):
    artist: str = None


@dataclass
class Album(BaseModel):
    mbid: str = None
    text: str = None
    name: str = None
    title: str = None
    playcount: int = None
    url: str = None
    artist: SimpleArtist = None
    image: List[Image] = None
    attr: Attributes = None


@dataclass
class Albums(BaseModel):
    album: List[Album]


@dataclass
class AlbumList(Albums, AttrModel):
    pass


@dataclass
class Chart(BaseModel):
    text: str
    from_date: str
    to_date: str


@dataclass
class Charts(BaseModel):
    chart: List[Chart]


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


@dataclass
class Tag(BaseModel):
    name: str
    url: str
    count: int = None


@dataclass
class TagInfo(BaseModel):
    name: str
    reach: int
    url: str = None
    taggings: int = None
    streamable: int = None
    count: int = None
    total: int = None
    wiki: Wiki = None


@dataclass
class TagInfoList(BaseModel):
    tag: List[TagInfo]
    attr: Attributes


@dataclass
class Tags(BaseModel):
    tag: List[Tag]


@dataclass
class TagList(Tags, AttrModel):
    pass


@dataclass
class Query(BaseModel):
    role: str
    page: int
    text: str
    search_terms: str = None


@dataclass
class OpenSearch(AttrModel):
    query: Query
    limit: int
    offset: int
    total: int

    def get_page(self):
        return self.query.page

    def get_limit(self):
        return self.limit

    def get_total(self):
        return self.total

    def get_total_pages(self):
        return ceil(self.total / self.limit)


@dataclass
class ChartList(Charts, AttrModel):
    pass
