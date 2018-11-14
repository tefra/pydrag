from pydrag.lastfm import Period, api
from pydrag.lastfm.models.common import (
    AlbumList,
    ArtistList,
    ChartList,
    TagList,
    TrackList,
)
from pydrag.lastfm.models.user import (
    ArtistTrackList,
    UserFriends,
    UserInfo,
    UserPersonalTags,
)


class UserService:
    """Last.fm User API interface for easy access/navigation."""

    def __init__(self, user: str):
        """
        user (Required) : The last.fm username to make api calls
        :param str user:
        """

        assert user is not None
        self.user = user

    @api.operation
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
        return dict(
            user=self.user,
            artist=artist,
            startTimestamp=from_date,
            endTimestamp=to_date,
            page=page,
        )

    @api.operation
    def get_friends(
        self, recent_tracks: bool, limit: int = 50, page: int = 1
    ) -> UserFriends:
        """
        Get a list of the user's friends on Last.fm.

        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: UserFriends
        """
        return dict(
            user=self.user, recenttracks=recent_tracks, page=page, limit=limit
        )

    @api.operation
    def get_info(self) -> UserInfo:
        """
        Get information about a user profile.

        :returns: UserInfo
        """
        return dict(user=self.user)

    @api.operation
    def get_loved_tracks(
        self, limit: int = 50, page: int = 1
    ) -> ArtistTrackList:
        """
        Get loved tracks list.

        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: TrackList
        """
        return dict(user=self.user, limit=limit, page=page)

    @api.operation
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

        return dict(
            user=self.user,
            tag=tag,
            taggingtype=tagging_type,
            limit=limit,
            page=page,
        )

    @api.operation
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
        return {
            "user": self.user,
            "from": from_date,
            "limit": limit,
            "page": page,
            "extended": extended,
            "to": to_date,
        }

    @api.operation
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
        return dict(
            user=self.user, limit=limit, page=page, period=period.value
        )

    @api.operation
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
        return dict(
            user=self.user, limit=limit, page=page, period=period.value
        )

    @api.operation
    def get_top_tags(self, limit: int = 50) -> TagList:
        """
        Get the top tags used by this user.

         :param int limit: Limit the number of tags returned
        :returns: TagList
        """
        return dict(user=self.user, limit=limit)

    @api.operation
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
        return dict(
            user=self.user, limit=limit, page=page, period=period.value
        )

    @api.operation
    def get_weekly_album_chart(
        self, from_date: str = None, to_date: str = None
    ) -> AlbumList:
        """
        :param from_date:  The date at which the chart should start from.
        :param to_date: The date at which the chart should end on.
        :returns: UserWeeklyAlbumChart
        """
        return {"user": self.user, "from": from_date, "to": to_date}

    @api.operation
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
        return {"user": self.user, "from": from_date, "to": to_date}

    @api.operation
    def get_weekly_chart_list(self) -> ChartList:
        """
        Get an artist chart for a user profile, for a given date range. If no
        date range is supplied, it will return the most recent artist chart for
        this user.

        :return: UserWeeklyChartList
        """
        return dict(user=self.user)

    @api.operation
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
        return {"user": self.user, "from": from_date, "to": to_date}
