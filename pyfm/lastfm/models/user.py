from typing import List, Optional

from attr import attrs

from pyfm import BaseModel


@attrs(auto_attribs=True)
class Image(BaseModel):
    size: str
    text: Optional[str] = None


@attrs(auto_attribs=True)
class Date(BaseModel):
    unixtime: int
    text: str


@attrs(auto_attribs=True)
class DateUTS(BaseModel):
    uts: str
    text: str


@attrs(auto_attribs=True)
class Attributes(BaseModel):
    rank: str = None
    date: str = None
    uts: str = None
    page: int = None
    perPage: int = None
    totalPages: int = None
    total: int = None
    user: str = None
    from_date: str = None
    to: str = None
    artist: str = None


@attrs(auto_attribs=True)
class Artist(BaseModel):
    mbid: str
    name: str = None
    text: str = None
    url: str = None
    playcount: str = None
    streamable: str = None
    image: List[Image] = None
    attr: Attributes = None


@attrs(auto_attribs=True)
class Album(BaseModel):
    mbid: str
    text: str = None
    name: str = None
    playcount: str = None
    url: str = None
    artist: Artist = None
    attr: Attributes = None
    image: List[Image] = None


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
    attr: Attributes = None


@attrs(auto_attribs=True)
class Track(BaseModel):
    name: str
    mbid: str
    playcount: str
    url: str
    artist: Artist
    image: List[Image]
    streamable: str = None  # super buggy
    duration: str = None
    attr: Attributes = None


@attrs(auto_attribs=True)
class UserInfo(BaseModel):
    playlists: str
    playcount: str
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
    attr: Attributes


@attrs(auto_attribs=True)
class UserFriends(BaseModel):
    user: List[UserInfo]
    attr: Attributes


@attrs(auto_attribs=True)
class UserLovedTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes


@attrs(auto_attribs=True)
class UserRecentTracks(BaseModel):
    track: List[ArtistTrack]
    attr: Attributes


@attrs(auto_attribs=True)
class UserTopAlbums(BaseModel):
    album: List[Album]
    attr: Attributes


@attrs(auto_attribs=True)
class UserTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes


@attrs(auto_attribs=True)
class UserTopTags(BaseModel):
    pass


@attrs(auto_attribs=True)
class UserPersonalTags(BaseModel):
    pass


@attrs(auto_attribs=True)
class UserTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes


@attrs(auto_attribs=True)
class UserWeeklyAlbumChart(BaseModel):
    album: List[Album]
    attr: Attributes


@attrs(auto_attribs=True)
class UserWeeklyArtistChart(BaseModel):
    artist: List[Artist]
    attr: Attributes


@attrs(auto_attribs=True)
class UserWeeklyTrackChart(BaseModel):
    track: List[Track]
    attr: Attributes


@attrs(auto_attribs=True)
class Chart(BaseModel):
    text: str
    from_date: str
    to: str


@attrs(auto_attribs=True)
class UserWeeklyChartList(BaseModel):
    chart: List[Chart]
    attr: Attributes
