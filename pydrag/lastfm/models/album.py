from typing import List

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import Album, OpenSearch, Tags, Tracks, Wiki


@dataclass
class AlbumInfo(Album):
    artist: str = None
    listeners: int = None
    tags: Tags = None
    streamable: int = None
    tracks: Tracks = None
    wiki: Wiki = None


@dataclass
class AlbumMatches(BaseModel):
    album: List[AlbumInfo]


@dataclass
class AlbumSearch(OpenSearch):
    matches: AlbumMatches
