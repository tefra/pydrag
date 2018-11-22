from typing import List, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm import Period
from pydrag.lastfm.models.common import (
    Album,
    AlbumList,
    Albums,
    ArtistList,
    Artists,
    Attributes,
    AttrModel,
    ChartList,
    Date,
    Image,
    SimpleArtist,
    TagList,
    TrackList,
    Tracks,
)

T = TypeVar("T", bound="User")


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
class UserPersonalTags(BaseModel):
    attr: Attributes
    tracks: Tracks = None
    albums: Albums = None
    artists: Artists = None


@dataclass
class User(BaseModel):
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

    @classmethod
    def find(cls, username: str) -> T:
        """
        Get information about a user profile.

        :returns: UserInfo
        """
        return cls.retrieve(params=dict(method="user.getInfo", user=username))

    def get_artists(self, limit: int = 50, page: int = 1) -> ArtistList:
        """
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: ArtistList
        """
        return self.retrieve(
            bind=ArtistList,
            params=dict(
                method="library.getArtists",
                user=self.name,
                page=page,
                limit=limit,
            ),
        )

    def get_artist_tracks(
        self,
        artist: str,
        from_date: str = None,
        to_date: str = None,
        page: int = 1,
    ) -> ArtistTrackList:
        """
        Get a list of tracks by a given artist scrobbled by this user,
        including scrobble time. Can be limited to specific timeranges,
        defaults to all time.

        :param artist: The artist name you are interested in
        :param from_date: An unix timestamp to start at.
        :param to_date: An unix timestamp to end at.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: UserArtistTracks
        """
        return self.retrieve(
            bind=ArtistTrackList,
            params=dict(
                method="user.getArtistTracks",
                user=self.name,
                artist=artist,
                startTimestamp=from_date,
                endTimestamp=to_date,
                page=page,
            ),
        )

    def get_friends(self, recent_tracks: bool, limit: int = 50, page: int = 1):
        """
        Get a list of the user's friends on Last.fm.

        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: UserFriends
        """
        return self.retrieve(
            bind=UserFriends,
            params=dict(
                method="user.getFriends",
                user=self.name,
                recenttracks=recent_tracks,
                page=page,
                limit=limit,
            ),
        )

    def get_loved_tracks(
        self, limit: int = 50, page: int = 1
    ) -> ArtistTrackList:
        """
        Get loved tracks list.

        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: TrackList
        """
        return self.retrieve(
            bind=ArtistTrackList,
            params=dict(
                method="user.getLovedTracks",
                user=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_personal_tags(
        self, tag: str, tagging_type: str, limit: int = 50, page: int = 1
    ) -> UserPersonalTags:
        """
        Get the user's personal tags.

        :param tag: The tag you're interested in.
        :param tagging_type: The type of items which have been tagged
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: UserPersonalTags
        """

        assert tagging_type in ("artist", "album", "track")

        return self.retrieve(
            bind=UserPersonalTags,
            params=dict(
                method="user.getPersonalTags",
                user=self.name,
                tag=tag,
                taggingtype=tagging_type,
                limit=limit,
                page=page,
            ),
        )

    def get_recent_tracks(
        self,
        extended: bool = True,
        from_date: str = None,
        to_date: str = None,
        limit: int = 50,
        page: int = 1,
    ) -> ArtistTrackList:
        """
        Get a list of the recent tracks listened to by this user. Also includes
        the currently playing track with the nowplaying="true" attribute if the
        user is currently listening.

        :param extended: Includes extended data in each artist, and whether or not the user has loved each track
        :param from_date: Beginning timestamp of a range - only display scrobbles after this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param to_date: End timestamp of a range - only display scrobbles before this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TrackList
        """
        return self.retrieve(
            bind=ArtistTrackList,
            params={
                "method": "user.getRecentTracks",
                "user": self.name,
                "from": from_date,
                "limit": limit,
                "page": page,
                "extended": extended,
                "to": to_date,
            },
        )

    def get_top_albums(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> AlbumList:
        """
        Get the top albums listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: UserTopAlbums
        """
        assert isinstance(period, Period)

        return self.retrieve(
            bind=AlbumList,
            params=dict(
                method="user.getTopAlbums",
                user=self.name,
                limit=limit,
                page=page,
                period=period.value,
            ),
        )

    def get_top_artists(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> ArtistList:
        """
        Get the top artists listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: ArtistList
        """
        assert isinstance(period, Period)
        return self.retrieve(
            bind=ArtistList,
            params=dict(
                method="user.getTopArtists",
                user=self.name,
                limit=limit,
                page=page,
                period=period.value,
            ),
        )

    def get_top_tags(self, limit: int = 50) -> TagList:
        """
        Get the top tags used by this user.

         :param int limit: Limit the number of tags returned
        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(method="user.getTopTags", user=self.name, limit=limit),
        )

    def get_top_tracks(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> TrackList:
        """
        Get the top tracks listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: UserTopTracks
        """

        assert isinstance(period, Period)
        return self.retrieve(
            bind=TrackList,
            params=dict(
                method="user.getTopTracks",
                user=self.name,
                limit=limit,
                page=page,
                period=period.value,
            ),
        )

    def get_weekly_album_chart(
        self, from_date: str = None, to_date: str = None
    ) -> AlbumList:
        """
        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :returns: UserWeeklyAlbumChart
        """
        return self.retrieve(
            bind=AlbumList,
            params={
                "method": "user.getWeeklyAlbumChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_artist_chart(
        self, from_date: str = None, to_date: str = None
    ) -> ArtistList:
        """
        Get an album chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent album chart for
        this user.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :returns: ArtistList
        """
        return self.retrieve(
            bind=ArtistList,
            params={
                "method": "user.getWeeklyArtistChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_chart_list(self) -> ChartList:
        """
        Get an artist chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent artist chart for
        this user.

        :return: UserWeeklyChartList
        """
        return self.retrieve(
            bind=ChartList,
            params=dict(method="user.getWeeklyChartList", user=self.name),
        )

    def get_weekly_track_chart(
        self, from_date: str = None, to_date: str = None
    ) -> TrackList:
        """
        Get a list of available charts for this user, expressed as date ranges
        which can be sent to the chart services.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :returns: UserWeeklyTrackChart
        """
        return self.retrieve(
            bind=TrackList,
            params={
                "method": "user.getWeeklyTrackChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )


@dataclass
class UserFriends(BaseModel):
    user: List[User]
    attr: Attributes = None
