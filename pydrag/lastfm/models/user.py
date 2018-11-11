from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.core import PaginatedModel
from pydrag.lastfm.models.common import (
    Album,
    Artist,
    Attributes,
    Chart,
    Date,
    DateUTS,
    Image,
    Tag,
    Track,
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
    scrobblesource: str = None
    realname: str = None
    recenttrack: ArtistTrack = None


@attrs(auto_attribs=True)
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserLovedTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserArtistTracks(UserLovedTracks):
    pass


@attrs(auto_attribs=True)
class UserRecentTracks(UserLovedTracks):
    pass


@attrs(auto_attribs=True)
class UserPersonalTagsAlbums(BaseModel):
    album: List[Album]


@attrs(auto_attribs=True)
class UserTopAlbums(UserPersonalTagsAlbums):
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyAlbumChart(UserTopAlbums):
    pass


@attrs(auto_attribs=True)
class UserPersonalTagsArtists(PaginatedModel):
    artist: List[Artist]


@attrs(auto_attribs=True)
class UserTopArtists(UserPersonalTagsArtists):
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyArtistChart(UserTopArtists):
    pass


@attrs(auto_attribs=True)
class UserTopTags(BaseModel):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserPersonalTagsTracks(PaginatedModel):
    track: List[Track]


@attrs(auto_attribs=True)
class UserTopTracks(UserPersonalTagsTracks):
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class UserWeeklyTrackChart(UserTopTracks):
    pass


@attrs(auto_attribs=True)
class UserPersonalTags(BaseModel):
    attr: Attributes = mattrib("@attr")
    tracks: UserPersonalTagsTracks = None
    albums: UserPersonalTagsAlbums = None
    artists: UserPersonalTagsArtists = None


@attrs(auto_attribs=True)
class UserWeeklyChartList(BaseModel):
    chart: List[Chart]
    attr: Attributes = mattrib("@attr")
