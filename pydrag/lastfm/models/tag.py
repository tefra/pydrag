from typing import List

from attr import attrs
from pydrag.lastfm.models import (
    Album,
    Artist,
    Attributes,
    BaseModel,
    Chart,
    Track,
    Wiki,
    mattrib,
)


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
class TagSimilar(BaseModel):
    tag: List[TagInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TagTopAlbums(BaseModel):
    album: List[Album]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TagTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TagTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TagTopTags(BaseModel):
    tag: List[TagInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TagWeeklyChartList(BaseModel):
    chart: List[Chart]
    attr: Attributes = mattrib("@attr")
