from typing import List

from attr import attrs

from lastfm.models import Attributes, Album, Artist, Track, Chart
from pyfm import BaseModel


@attrs(auto_attribs=True)
class Wiki(BaseModel):
    content: str
    summary: str


@attrs(auto_attribs=True)
class TagInfo(BaseModel):
    name: str
    reach: int
    count: int = None
    total: int = None
    wiki: Wiki = None


@attrs(auto_attribs=True)
class TagSimilar(BaseModel):
    tag: List[TagInfo]
    attr: Attributes


@attrs(auto_attribs=True)
class TagTopAlbums(BaseModel):
    album: List[Album]
    attr: Attributes


@attrs(auto_attribs=True)
class TagTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes


@attrs(auto_attribs=True)
class TagTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes


@attrs(auto_attribs=True)
class TagTopTags(BaseModel):
    tag: List[TagInfo]
    attr: Attributes


@attrs(auto_attribs=True)
class TagWeeklyChartList(BaseModel):
    chart: List[Chart]
    attr: Attributes
