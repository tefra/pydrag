from typing import List, Optional, Union

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.constants import Period
from pydrag.lastfm.models.album import Album
from pydrag.lastfm.models.artist import Artist
from pydrag.lastfm.models.common import Chart, Date, Image
from pydrag.lastfm.models.tag import Tag
from pydrag.lastfm.models.track import Track


@dataclass
class User(BaseModel):
    """
    Last.FM user and user library api client.

    :param playcount: Total track playcount
    :param gender: Gender
    :param name: Display name
    :param url: Last.fm profile url
    :param country: Country name
    :param image: User's avatar in multiple sizes
    :param age: Self explanatory
    :param registered: Registraton date
    :param real_name: The full name
    :param recent_track: User's most recent scrobble track
    """

    playlists: int
    playcount: int
    gender: str
    name: str
    url: str
    country: str
    image: List[Image]
    age: int
    registered: Date
    real_name: Optional[str] = None
    recent_track: Optional[Track] = None

    @classmethod
    def from_dict(cls, data: dict):
        data.update(
            dict(
                registered=Date.from_dict(data["registered"]),
                image=list(map(Image.from_dict, data["image"])),
            )
        )
        if "real_name" in data:
            data["real_name"] = str(data["real_name"])
        if "recent_track" in data:
            data["recent_track"] = Track.from_dict(data["recent_track"])
        return super(User, cls).from_dict(data)

    @classmethod
    def find(cls, username: str) -> "User":
        """
        Get information about a user profile.

        :rtype: :class:`~pydrag.lastfm.models.user.User`
        """
        return cls.retrieve(params=dict(method="user.getInfo", user=username))

    def get_artists(self, limit: int = 50, page: int = 1) -> List[Artist]:
        """
        Retrieve a paginated list of all the artists in the user's library,
        with playcounts and tagcounts.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            many="artist",
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
    ) -> List[Track]:
        """
        Get a list of tracks by a given artist scrobbled by this user,
        including scrobble time. Can be limited to specific timeranges,
        defaults to all time.

        :param artist: The artist name you are interested in
        :param from_date: An unix timestamp to start at.
        :param to_date: An unix timestamp to end at.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            many="track",
            params=dict(
                method="user.getArtistTracks",
                user=self.name,
                artist=artist,
                startTimestamp=from_date,
                endTimestamp=to_date,
                page=page,
            ),
        )

    def get_friends(
        self, recent_tracks: bool, limit: int = 50, page: int = 1
    ) -> List["User"]:
        """
        Get a list of the user's friends on Last.fm.

        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.user.User`
        """
        return self.retrieve(
            bind=User,
            many="user",
            params=dict(
                method="user.getFriends",
                user=self.name,
                recenttracks=recent_tracks,
                page=page,
                limit=limit,
            ),
        )

    def get_loved_tracks(self, limit: int = 50, page: int = 1) -> List[Track]:
        """
        Get the user's loved tracks list.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            many="track",
            params=dict(
                method="user.getLovedTracks",
                user=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_personal_tags(
        self, tag: str, type: str, limit: int = 50, page: int = 1
    ) -> List[Union[Artist, Track, Album]]:
        """
        Get the user's personal tags.

        :param tag: The tag you're interested in.
        :param type: The type of items which have been tagged
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`  or :class:`~pydrag.lastfm.models.artist.Artist` or :class:`~pydrag.lastfm.models.album.Album`
        """

        map = dict(artist=Artist, album=Album, track=Track)
        bind = map.get(type)
        assert bind is not None

        return self.retrieve(
            bind=bind,
            many=("{}s".format(type), type),
            params=dict(
                method="user.getPersonalTags",
                user=self.name,
                tag=tag,
                taggingtype=type,
                limit=limit,
                page=page,
            ),
        )

    def get_recent_tracks(
        self,
        from_date: str = None,
        to_date: str = None,
        limit: int = 50,
        page: int = 1,
    ) -> List[Track]:
        """
        Get a list of the recent tracks listened to by this user. Also includes
        the currently playing track with the nowplaying="true" attribute if the
        user is currently listening.

        :param from_date: Beginning timestamp of a range - only display scrobbles after this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param to_date: End timestamp of a range - only display scrobbles before this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            many="track",
            params={
                "method": "user.getRecentTracks",
                "user": self.name,
                "from": from_date,
                "limit": limit,
                "page": page,
                "extended": True,
                "to": to_date,
            },
        )

    def get_top_albums(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> List[Album]:
        """
        Get the top albums listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.album.Album`
        :rtype: List[Album]
        """
        assert isinstance(period, Period)

        return self.retrieve(
            bind=Album,
            many="album",
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
    ) -> List[Artist]:
        """
        Get the top artists listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        assert isinstance(period, Period)
        return self.retrieve(
            bind=Artist,
            many="artist",
            params=dict(
                method="user.getTopArtists",
                user=self.name,
                limit=limit,
                page=page,
                period=period.value,
            ),
        )

    def get_top_tags(self, limit: int = 50) -> List[Tag]:
        """
        Get the top tags used by this user.

        :param limit: Limit the number of tags returned
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.tag.Tag`
        :rtype: List[Tag]
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(method="user.getTopTags", user=self.name, limit=limit),
        )

    def get_top_tracks(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> List[Track]:
        """
        Get the top tracks listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """

        assert isinstance(period, Period)
        return self.retrieve(
            bind=Track,
            many="track",
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
    ) -> List[Album]:
        """
        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.album.Album`
        """
        return self.retrieve(
            bind=Album,
            many="album",
            params={
                "method": "user.getWeeklyAlbumChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_artist_chart(
        self, from_date: str = None, to_date: str = None
    ) -> List[Artist]:
        """
        Get an album chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent album chart for
        this user.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            many="artist",
            params={
                "method": "user.getWeeklyArtistChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_chart_list(self) -> List[Chart]:
        """
        Get an artist chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent artist chart for
        this user.

        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.common.Chart`
        """
        return self.retrieve(
            bind=Chart,
            many="chart",
            params=dict(method="user.getWeeklyChartList", user=self.name),
        )

    def get_weekly_track_chart(
        self, from_date: str = None, to_date: str = None
    ) -> List[Track]:
        """
        Get a list of available charts for this user, expressed as date ranges
        which can be sent to the chart services.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            many="track",
            params={
                "method": "user.getWeeklyTrackChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )
