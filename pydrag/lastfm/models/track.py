from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.album import AlbumInfo
from pydrag.lastfm.models.common import (
    Artist,
    Attributes,
    OpenSearch,
    Tags,
    TagsAttr,
    TracksAttr,
    TrackSimpleArtist,
    Wiki,
)


@attrs(auto_attribs=True)
class TrackTopTags(TagsAttr):
    pass


@attrs(auto_attribs=True)
class TrackTags(TagsAttr):
    pass


@attrs(auto_attribs=True)
class TrackTopTracks(TracksAttr):
    pass


@attrs(auto_attribs=True)
class TrackSimilar(TracksAttr):
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
    toptags: Tags = None
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
    trackmatches: TrackMatches


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
    ignoredMessage: Corrected = None
    albumArtist: Corrected = None
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
    streamId: str = None
    chosenByUser: bool = True
    trackNumber: str = None
    mbid: str = None
    albumArtist: str = None
    duration: int = None
