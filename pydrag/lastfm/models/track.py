from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.album import AlbumInfo
from pydrag.lastfm.models.common import (
    Artist,
    Attributes,
    AttrModel,
    OpenSearch,
    Tags,
    Tracks,
    TrackSimpleArtist,
    Wiki,
)


@attrs(auto_attribs=True)
class TrackTopTags(Tags, AttrModel):
    pass


@attrs(auto_attribs=True)
class TrackTags(Tags, AttrModel):
    pass


@attrs(auto_attribs=True)
class TrackTopTracks(Tracks, AttrModel):
    pass


@attrs(auto_attribs=True)
class TrackSimilar(Tracks, AttrModel):
    pass


@attrs(auto_attribs=True)
class TrackInfo(BaseModel):
    album: AlbumInfo = None
    artist: Artist = None
    bio: Wiki = None
    attr: Attributes = mattrib("@attr", default=None)
    duration: int = None
    listeners: int = None
    mbid: str = None
    name: str = None
    playcount: int = None
    top_tags: Tags = mattrib("toptags", default=None)
    url: str = None
    wiki: Wiki = None


@attrs(auto_attribs=True)
class CorrectionTrack(BaseModel):
    attr: Attributes = mattrib("@attr")
    track: TrackInfo = None


@attrs(auto_attribs=True)
class TrackCorrection(BaseModel):
    correction: CorrectionTrack


@attrs(auto_attribs=True)
class TrackMatches(BaseModel):
    track: List[TrackSimpleArtist]


@attrs(auto_attribs=True)
class TrackSearch(OpenSearch):
    matches: TrackMatches = mattrib("trackmatches")


@attrs(auto_attribs=True)
class Corrected(BaseModel):
    text: str = mattrib("#text", default=None)
    code: str = None
    corrected: int = None


@attrs(auto_attribs=True)
class TrackUpdateNowPlaying(BaseModel):
    album: Corrected = None
    artist: Corrected = None
    track: Corrected = None
    timestamp: int = None
    ignored_message: Corrected = mattrib("ignoredMessage", default=None)
    album_artist: Corrected = mattrib("albumArtist", default=None)
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class TrackScrobble(BaseModel):
    scrobble: List[TrackUpdateNowPlaying]
    attr: Attributes = mattrib("@attr")

    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data, dict) and data.get("scrobble"):
            if isinstance(data["scrobble"], dict):
                data["scrobble"] = [data["scrobble"]]
        return super().from_dict(data)


@attrs(auto_attribs=True)
class ScrobbleTrack(BaseModel):
    artist: str
    track: str
    timestamp: int
    album: str = None
    context: str = None
    stream_id: str = mattrib("albumArtist", default=None)
    chosen_by_user: bool = mattrib("ignoredMessage", default=True)
    track_number: str = mattrib("ignoredMessage", default=None)
    mbid: str = None
    album_artist: str = mattrib("albumArtist", default=None)
    duration: int = None
