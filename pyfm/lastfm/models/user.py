from typing import List

from attr import attrs

from pyfm.lastfm.models import (
    Attributes,
    Artist,
    Image,
    DateUTS,
    Date,
    Track,
    Album,
    Chart,
    Tag,
    mattrib,
)
from pyfm import BaseModel


@attrs(auto_attribs=True)
class ArtistTrack(BaseModel):
    artist: Artist
    name: str
    mbid: str
    url: str
    album: Album = None
    streamable: str = None  # super buggy
    image: List[Image] = None
    date: DateUTS = None
    attr: Attributes = mattrib("@attr", default=None)


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
    scrobblesource: str = None
    realname: str = None
    recenttrack: ArtistTrack = None


@attrs(auto_attribs=True)
class UserArtistTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserLovedTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserRecentTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserTopAlbums(BaseModel):
    album: List[Album]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserTopTags(BaseModel):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserPersonalTagsTracks(BaseModel):
    track: List[Track]


@attrs(auto_attribs=True)
class UserPersonalTagsAlbums(BaseModel):
    album: List[Album]


@attrs(auto_attribs=True)
class UserPersonalTagsArtists(BaseModel):
    artist: List[Artist]


@attrs(auto_attribs=True)
class UserPersonalTags(BaseModel):
    attr: Attributes = mattrib("@attr")
    tracks: UserPersonalTagsTracks = None
    albums: UserPersonalTagsAlbums = None
    artists: UserPersonalTagsArtists = None


@attrs(auto_attribs=True)
class UserTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyAlbumChart(BaseModel):
    album: List[Album]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyArtistChart(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyTrackChart(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyChartList(BaseModel):
    chart: List[Chart]
    attr: Attributes = mattrib("@attr")
