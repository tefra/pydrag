from typing import List

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import (
    Album,
    Albums,
    Artists,
    Attributes,
    AttrModel,
    Date,
    Image,
    SimpleArtist,
    Tracks,
)


@dataclass
class ArtistTrack(BaseModel):
    artist: SimpleArtist
    name: str
    mbid: str
    url: str
    album: Album = None
    streamable: str = None  # super buggy
    image: List[Image] = None
    date: Date = None
    attr: Attributes = None


@dataclass
class ArtistTrackList(AttrModel):
    track: List[ArtistTrack]


@dataclass
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
    source: str = None
    real_name: str = None
    recent_track: ArtistTrack = None


@dataclass
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes = None


@dataclass
class UserPersonalTags(BaseModel):
    attr: Attributes
    tracks: Tracks = None
    albums: Albums = None
    artists: Artists = None
