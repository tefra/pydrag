from lastfm.methods import Limit, Page, Date, apimethod


class User:
    def __init__(self, user: str):
        """
        user (Required) : The last.fm username to make api calls
        :param str user:
        """
        self.user = user

    @apimethod
    def get_artist_tracks(
        self,
        artist: str,
        from_date: Date = None,
        to_date: Date = None,
        page: Page = None,
    ):
        """
        :param artist: The artist name you are interested in
        :param from_date: An unix timestamp to start at.
        :param to_date: An unix timestamp to end at.
        :param page: The page number to fetch. Defaults to first page.
        :return: dict
        """
        return dict(
            user=self.user,
            artist=artist,
            startTimestamp=from_date,
            endTimestamp=to_date,
            page=page,
        )

    @apimethod
    def get_friends(
        self, recent_tracks: bool, limit: Limit = None, page: Page = None
    ):
        """
        :param recent_tracks: Whether or not to include information about
         friends' recent listening in the response.
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :return: dict
        """
        return dict(
            user=self.user, recenttracks=recent_tracks, page=page, limit=limit
        )

    @apimethod
    def get_info(self):
        """
        :return: Request
        """
        return dict(user=self.user)

    @apimethod
    def get_loved_tracks(self, limit: Limit = None, page: Page = None):
        """
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :return: dict
        """
        return dict(user=self.user, limit=limit, page=page)

    @apimethod
    def get_personal_tags(
        self,
        tag: str,
        tagging_type: str,
        limit: Limit = None,
        page: Page = None,
    ):
        """
        :param tag: The tag you're interested in.
        :param tagging_type: The type of items which have been tagged
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :return:
        """

        assert tagging_type in ("artist", "album", "track")

        return dict(
            user=self.user,
            tag=tag,
            taggingtype=tagging_type,
            limit=limit,
            page=page,
        )

    @apimethod
    def get_recent_tracks(
        self,
        extended: bool = True,
        from_date: Date = None,
        to_date: Date = None,
        limit: Limit = None,
        page: Page = None,
    ):
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
        :param limit:
        :param page:
        :return:
        """
        return {
            "user": self.user,
            "from": from_date,
            "limit": limit,
            "page": page,
            "extended": extended,
            "to": to_date,
        }

    @apimethod
    def get_top_albums(
        self, period: str, limit: Limit = None, page: Page = None
    ):
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top albums for.
        :param limit:
        :param page:
        :return:
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @apimethod
    def get_top_artists(
        self, period: str, limit: Limit = None, page: Page = None
    ):
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top artists for.
        :param limit:
        :param page:
        :return:
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @apimethod
    def get_top_tags(self, limit: Limit = None):
        """
         :param limit: Limit the number of tags returned
        :return:
        """
        return dict(user=self.user, limit=limit)

    @apimethod
    def get_top_tracks(
        self, period: str, limit: Limit = None, page: Page = None
    ):
        """
        :param period: overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top tracks for.
        :param limit:
        :param page:
        :return:
        """
        return dict(user=self.user, limit=limit, page=page, period=period)

    @apimethod
    def get_weekly_album_chart(
        self, from_date: Date = None, to_date: Date = None
    ):
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :return:
        """
        return {"user": self.user, "from": from_date, "to": to_date}

    @apimethod
    def get_weekly_artist_chart(
        self, from_date: Date = None, to_date: Date = None
    ):
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :return:
        """
        return {"user": self.user, "from": from_date, "to": to_date}

    @apimethod
    def get_weekly_chart_list(self):
        return dict(user=self.user, limit=10)

    @apimethod
    def get_weekly_track_chart(
        self, from_date: Date = None, to_date: Date = None
    ):
        """
        :param from_date:  The date at which the chart should start from. See User.getWeeklyChartList for more.
        :param to_date: The date at which the chart should end on. See User.getWeeklyChartList for more.
        :return:
        """
        return {"user": self.user, "from": from_date, "to": to_date}


if __name__ == "__main__":
    response = User(user="Zaratoustre").get_info()
