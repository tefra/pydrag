from typing import List

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.album import AlbumInfo
from pydrag.lastfm.models.common import (
    Attributes,
    OpenSearch,
    Tags,
    Track,
    TrackSimpleArtist,
    Wiki,
)


@dataclass
class TrackInfo(Track):
    wiki: Wiki = None
    album: AlbumInfo = None
    top_tags: Tags = None


@dataclass
class CorrectionTrack(BaseModel):
    attr: Attributes
    track: TrackInfo = None


@dataclass
class TrackCorrection(BaseModel):
    correction: CorrectionTrack


@dataclass
class TrackMatches(BaseModel):
    track: List[TrackSimpleArtist]


@dataclass
class TrackSearch(OpenSearch):
    matches: TrackMatches


@dataclass
class Corrected(BaseModel):
    text: str = None
    code: str = None
    corrected: int = None


@dataclass
class TrackUpdateNowPlaying(BaseModel):
    album: Corrected = None
    artist: Corrected = None
    track: Corrected = None
    timestamp: int = None
    ignored_message: Corrected = None
    album_artist: Corrected = None
    attr: Attributes = None


@dataclass
class TrackScrobble(BaseModel):
    scrobble: List[TrackUpdateNowPlaying]
    attr: Attributes

    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data, dict) and data.get("scrobble"):
            if isinstance(data["scrobble"], dict):
                data["scrobble"] = [data["scrobble"]]
        return super().from_dict(data)


@dataclass
class ScrobbleTrack(BaseModel):
    artist: str
    track: str
    timestamp: int
    album: str = None
    context: str = None
    stream_id: str = None
    chosen_by_user: bool = None
    track_number: str = None
    mbid: str = None
    album_artist: str = None
    duration: int = None
