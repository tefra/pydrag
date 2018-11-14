from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import Album, OpenSearch, Tags, Tracks, Wiki


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
class AlbumSearch(OpenSearch):
    matches: AlbumMatches = mattrib("albummatches")
