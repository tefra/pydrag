from datetime import datetime
from typing import Dict, List, Optional, Union

from attr import dataclass

from pydrag.constants import Period
from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.common import BaseModel, Chart, Image, ListModel
from pydrag.models.tag import Tag
from pydrag.models.track import Track
from pydrag.services import ApiMixin


@dataclass
class User(BaseModel, ApiMixin):
    """
    Last.FM user and user library api wrapper.

    :param playcount: Total track playcount
    :param gender: Gender
    :param name: Display name
    :param url: Last.fm profile url
    :param country: Country name
    :param image: User's avatar in multiple sizes
    :param age: Self explanatory
    :param registered: Unix timestamp of the registration date
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
    registered: int
    real_name: Optional[str] = None
    recent_track: Optional[Track] = None

    @property
    def date_registered(self) -> datetime:
        """
        Return a datetime instance of the user's registration date.

        :rtype: :class:`datetime.datetime`
        """
        return datetime.utcfromtimestamp(self.registered)

    @classmethod
    def from_dict(cls, data: Dict):
        data.update(
            dict(
                registered=data["registered"]["timestamp"],
                image=list(map(Image.from_dict, data["image"])),
            )
        )
        if "recent_track" in data:
            data["recent_track"] = Track.from_dict(data["recent_track"])
        return super(User, cls).from_dict(data)

    @classmethod
    def find(cls, username: str) -> "User":
        """
        Get information about a user profile.

        :rtype: :class:`~pydrag.models.user.User`
        """
        return cls.retrieve(
            bind=User, params=dict(method="user.getInfo", user=username)
        )

    def get_artists(self, limit: int = 50, page: int = 1) -> ListModel[Artist]:
        """
        Retrieve a paginated list of all the artists in the user's library,
        with playcounts and tagcounts.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            flatten="artist",
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
    ) -> ListModel[Track]:
        """
        Get a list of tracks by a given artist scrobbled by this user,
        including scrobble time. Can be limited to specific timeranges,
        defaults to all time.

        :param artist: The artist name you are interested in
        :param from_date: An unix timestamp to start at.
        :param to_date: An unix timestamp to end at.
        :param page: The page number to fetch.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            flatten="track",
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
    ) -> ListModel["User"]:
        """
        Get a list of the user's friends on Last.fm.

        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.user.User`
        """
        return self.retrieve(
            bind=User,
            flatten="user",
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
    ) -> ListModel[Track]:
        """
        Get the user's loved tracks list.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            flatten="track",
            params=dict(
                method="user.getLovedTracks",
                user=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_personal_tags(
        self, tag: str, category: str, limit: int = 50, page: int = 1
    ) -> ListModel[Union[Artist, Track, Album]]:
        """
        Get the user's personal tags.

        :param tag: The tag you're interested in.
        :param category: The type of items which have been tagged
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`  or :class:`~pydrag.models.artist.Artist` or :class:`~pydrag.models.album.Album`
        """

        valid_categories = dict(artist=Artist, album=Album, track=Track)
        bind = valid_categories.get(category)
        if bind is None:
            raise ValueError("Provide a tag type: artist, album or track!")

        return self.retrieve(
            bind=bind,
            flatten="{0}s.{0}".format(category),
            params=dict(
                method="user.getPersonalTags",
                user=self.name,
                tag=tag,
                taggingtype=category,
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
    ) -> ListModel[Track]:
        """
        Get a list of the recent tracks listened to by this user. Also includes
        the currently playing track with the nowplaying="true" attribute if the
        user is currently listening.

        :param from_date: Beginning timestamp of a range - only display scrobbles after this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param to_date: End timestamp of a range - only display scrobbles before this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            flatten="track",
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
    ) -> ListModel[Album]:
        """
        Get the top albums listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`~pydrag.models.common.ListModel` of :class:`~pydrag.models.album.Album`
        :rtype: List[Album]
        """
        if not isinstance(period, Period):
            raise ValueError("Invalid period")

        return self.retrieve(
            bind=Album,
            flatten="album",
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
    ) -> ListModel[Artist]:
        """
        Get the top artists listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.artist.Artist`
        """
        if not isinstance(period, Period):
            raise ValueError("Invalid period")

        return self.retrieve(
            bind=Artist,
            flatten="artist",
            params=dict(
                method="user.getTopArtists",
                user=self.name,
                limit=limit,
                page=page,
                period=period.value,
            ),
        )

    def get_top_tags(self, limit: int = 50) -> ListModel[Tag]:
        """
        Get the top tags used by this user.

        :param limit: Limit the number of tags returned
        :rtype: :class:`~pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        :rtype: List[Tag]
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params=dict(method="user.getTopTags", user=self.name, limit=limit),
        )

    def get_top_tracks(
        self, period: Period, limit: int = 50, page: int = 1
    ) -> ListModel[Track]:
        """
        Get the top tracks listened to by a user. You can stipulate a time
        period.

        :param Period period:
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """

        if not isinstance(period, Period):
            raise ValueError("Invalid period")

        return self.retrieve(
            bind=Track,
            flatten="track",
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
    ) -> ListModel[Album]:
        """
        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.album.Album`
        """
        return self.retrieve(
            bind=Album,
            flatten="album",
            params={
                "method": "user.getWeeklyAlbumChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_artist_chart(
        self, from_date: str = None, to_date: str = None
    ) -> ListModel[Artist]:
        """
        Get an album chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent album chart for
        this user.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            flatten="artist",
            params={
                "method": "user.getWeeklyArtistChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )

    def get_weekly_chart_list(self) -> ListModel[Chart]:
        """
        Get an artist chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent artist chart for
        this user.

        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.common.Chart`
        """
        return self.retrieve(
            bind=Chart,
            flatten="chart",
            params=dict(method="user.getWeeklyChartList", user=self.name),
        )

    def get_weekly_track_chart(
        self, from_date: str = None, to_date: str = None
    ) -> ListModel[Track]:
        """
        Get a list of available charts for this user, expressed as date ranges
        which can be sent to the chart services.

        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :rtype: :class:`~models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            flatten="track",
            params={
                "method": "user.getWeeklyTrackChart",
                "user": self.name,
                "from": from_date,
                "to": to_date,
            },
        )
