from typing import List

from attr import attrs

from pyfm import BaseModel, mattrib, T
from pyfm.lastfm.models import (
    Attributes,
    Wiki,
    Tag,
    Track,
    Query,
    AlbumInfo,
    Artist,
    TrackSimpleArtist,
)


@attrs(auto_attribs=True)
class TrackTopTags(BaseModel):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tags(BaseModel):
    tag: List[Tag] = None


@attrs(auto_attribs=True)
class TrackTags(Tags):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tracks(BaseModel):
    track: List[Track] = None


@attrs(auto_attribs=True)
class SimilarTrack(BaseModel):
    artist: List[Track]


@attrs(auto_attribs=True)
class TrackStat(BaseModel):
    listeners: int
    playcount: int


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
class TrackSearch(BaseModel):
    trackmatches: TrackMatches
    query: Query = mattrib("opensearch:Query")
    itemsPerPage: int = mattrib("opensearch:itemsPerPage")
    startIndex: int = mattrib("opensearch:startIndex")
    totalResults: int = mattrib("opensearch:totalResults")
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TrackTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class TrackSimilar(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


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
    def from_dict(cls: T, data: dict) -> T:
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
