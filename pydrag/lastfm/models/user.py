from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import (
    Album,
    Albums,
    Artists,
    Attributes,
    AttrModel,
    Date,
    DateUTS,
    Image,
    SimpleArtist,
    Tracks,
)


@attrs(auto_attribs=True)
class ArtistTrack(BaseModel):
    artist: SimpleArtist
    name: str
    mbid: str
    url: str
    album: Album = None
    streamable: str = None  # super buggy
    image: List[Image] = None
    date: DateUTS = None
    attr: Attributes = mattrib("@attr", default=None)


@attrs(auto_attribs=True)
class ArtistTrackList(AttrModel):
    track: List[ArtistTrack]


@attrs(auto_attribs=True)
class UserInfo(BaseModel):
    playlists: str
    playcount: int
    gender: str
    name: str
    subscriber: str
    url: str
    country: str
    image: List[Image]
    type: str
    age: str
    bootstrap: str
    registered: Date
    source: str = mattrib("scrobblesource", default=None)
    real_name: str = mattrib("realname", default=None)
    recent_track: ArtistTrack = mattrib("recenttrack", default=None)


@attrs(auto_attribs=True)
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserPersonalTags(BaseModel):
    attr: Attributes = mattrib("@attr")
    tracks: Tracks = None
    albums: Albums = None
    artists: Artists = None
