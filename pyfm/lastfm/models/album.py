from typing import List

from attr import attrs

from pyfm import BaseModel, mattrib
from pyfm.lastfm.models import Attributes, Album, Wiki, Tag, Track, Query


@attrs(auto_attribs=True)
class AlbumTopTags(BaseModel):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tags(BaseModel):
    tag: List[Tag] = None


@attrs(auto_attribs=True)
class AlbumTags(Tags):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tracks(BaseModel):
    track: List[Track] = None


@attrs(auto_attribs=True)
class AlbumInfo(Album):
    artist: str = None
    listeners: int = None
    tags: Tags = None
    tracks: Tracks = None
    wiki: Wiki = None


@attrs(auto_attribs=True)
class AlbumMatches(BaseModel):
    album: List[AlbumInfo]


@attrs(auto_attribs=True)
class AlbumSearch(BaseModel):
    albummatches: AlbumMatches
    query: Query = mattrib("opensearch:Query")
    itemsPerPage: int = mattrib("opensearch:itemsPerPage")
    startIndex: int = mattrib("opensearch:startIndex")
    totalResults: int = mattrib("opensearch:totalResults")
    attr: Attributes = mattrib("@attr")
