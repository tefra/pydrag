from typing import List, Optional

from attr import dataclass

from pydrag.core import BaseModel


@dataclass
class CorrectionAttributes(BaseModel):
    index: int = None
    track_corrected: int = None
    artist_corrected: int = None


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


@dataclass
class AttrModel(BaseModel):
    attr: RootAttributes


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
class TrackList(AttrModel):
    track: List[Track]


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
class TagInfoList(AttrModel):
    tag: List[TagInfo]


@dataclass
class TagList(AttrModel):
    tag: List[Tag]


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


@dataclass
class ChartList(Charts, AttrModel):
    pass
