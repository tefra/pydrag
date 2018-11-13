from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import (
    Album,
    Albums,
    Artist,
    Artists,
    Attributes,
    AttrModel,
    Charts,
    Date,
    DateUTS,
    Image,
    Tags,
    Tracks,
)


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
    source: str = mattrib("scrobblesource", default=None)
    real_name: str = mattrib("realname", default=None)
    recent_track: ArtistTrack = mattrib("recenttrack", default=None)


@attrs(auto_attribs=True)
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserLovedTracks(AttrModel):
    track: List[ArtistTrack]


class UserArtistTracks(UserLovedTracks):
    pass


class UserRecentTracks(UserLovedTracks):
    pass


class UserPersonalTagsAlbums(Albums):
    pass


@attrs(auto_attribs=True)
class UserTopAlbums(Albums, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserWeeklyAlbumChart(Albums, AttrModel):
    pass


class UserPersonalTagsArtists(Artists):
    pass


@attrs(auto_attribs=True)
class UserTopArtists(Artists, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserWeeklyArtistChart(Artists, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserTopTags(Tags, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserPersonalTagsTracks(Tracks):
    pass


@attrs(auto_attribs=True)
class UserTopTracks(Tracks, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserWeeklyTrackChart(Tracks, AttrModel):
    pass


@attrs(auto_attribs=True)
class UserPersonalTags(BaseModel):
    attr: Attributes = mattrib("@attr")
    tracks: UserPersonalTagsTracks = None
    albums: UserPersonalTagsAlbums = None
    artists: UserPersonalTagsArtists = None


@attrs(auto_attribs=True)
class UserWeeklyChartList(Charts, AttrModel):
    pass
