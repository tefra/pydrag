from pyfm.lastfm import api
from pyfm.lastfm.models import (
    UserArtistTracks,
    UserFriends,
    UserInfo,
    UserLovedTracks,
    UserPersonalTags,
    UserRecentTracks,
    UserTopAlbums,
    UserTopArtists,
    UserTopTags,
    UserTopTracks,
    UserWeeklyAlbumChart,
    UserWeeklyArtistChart,
    UserWeeklyChartList,
    UserWeeklyTrackChart,
)


class User:
    """
    Last.fm User API interface for easy access/navigation
    """

    def __init__(self, user: str):
        """
        user (Required) : The last.fm username to make api calls
        :param str user:
        """
        self.user = user

    @api.operation
    def get_artist_tracks(
        self,
        artist: str,
        from_date: str = None,
        to_date: str = None,
        page: int = 1,
    ) -> UserArtistTracks:
        """
        :param artist: The artist name you are interested in
        :param from_date: An unix timestamp to start at.
        :param to_date: An unix timestamp to end at.
        :param page: The page number to fetch. Defaults to first page.
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
        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :returns: UserFriends
        """
        return dict(
            user=self.user, recenttracks=recent_tracks, page=page, limit=limit
        )

    @api.operation
    def get_info(self) -> UserInfo:
        """
        :returns: UserInfo
        """
        return dict(user=self.user)

    @api.operation
    def get_loved_tracks(
        self, limit: int = 50, page: int = 1
    ) -> UserLovedTracks:
        """
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :returns: UserLovedTracks
        """
        return dict(user=self.user, limit=limit, page=page)

    @api.operation
    def get_personal_tags(
        self, tag: str, tagging_type: str, limit: int = 50, page: int = 1
    ) -> UserPersonalTags:
        """
        :param tag: The tag you're interested in.
        :param tagging_type: The type of items which have been tagged
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
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
    ) -> UserRecentTracks:
        """
        :param extended: Includes extended data in each artist, and whether or
         not the user has loved each track
        :param from_date: Beginning timestamp of a range - only display
        scrobbles after this time, in UNIX timestamp format (integer number
         of seconds since 00:00:00, January 1st 1970 UTC).
         This must be in the UTC time zone.

        :param to_date: End timestamp of a range - only display scrobbles
        before this time, in UNIX timestamp format
        (integer number of seconds since 00:00:00, January 1st 1970 UTC).
        This must be in the UTC time zone.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: UserRecentTracks
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
        self, period: str, limit: int = 50, page: int = 1
    ) -> UserTopAlbums:
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top albums for.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: UserTopAlbums
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @api.operation
    def get_top_artists(
        self, period: str, limit: int = 50, page: int = 1
    ) -> UserTopArtists:
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top artists for.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: UserTopArtists
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @api.operation
    def get_top_tags(self, limit: int = 50) -> UserTopTags:
        """
         :param limit: Limit the number of tags returned
        :returns: UserTopTags
        """
        return dict(user=self.user, limit=limit)

    @api.operation
    def get_top_tracks(
        self, period: str, limit: int = 50, page: int = 1
    ) -> UserTopTracks:
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top tracks for.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: UserTopTracks
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @api.operation
    def get_weekly_album_chart(
        self, from_date: str = None, to_date: str = None
    ) -> UserWeeklyAlbumChart:
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :returns: UserWeeklyAlbumChart
        """
        return {"user": self.user, "from": from_date, "to": to_date}

    @api.operation
    def get_weekly_artist_chart(
        self, from_date: str = None, to_date: str = None
    ) -> UserWeeklyArtistChart:
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :returns: UserWeeklyArtistChart
        """
        return {"user": self.user, "from": from_date, "to": to_date}

    @api.operation
    def get_weekly_chart_list(self) -> UserWeeklyChartList:
        """
        :return: UserWeeklyChartList
        """
        return dict(user=self.user)

    @api.operation
    def get_weekly_track_chart(
        self, from_date: str = None, to_date: str = None
    ) -> UserWeeklyTrackChart:
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :returns: UserWeeklyTrackChart
        """
        return {"user": self.user, "from": from_date, "to": to_date}
