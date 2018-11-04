import datetime


class User:
    def getArtistTracks(self, user: str, artist: str):
        """
        user (Required) : The last.fm username to fetch the recent tracks of.
        artist (Required) : The artist name you are interested in
        startTimestamp (Optional) : An unix timestamp to start at.
        page (Optional) : The page number to fetch. Defaults to first page.
        endTimestamp (Optional) : An unix timestamp to end at.
        :param user:
        :param artist:
        :return:
        """
        pass

    def getFriends(self, user: str, recenttracks: bool):
        """
        user (Required) : The last.fm username to fetch the friends of.
        recenttracks (Optional) : Whether or not to include information about friends' recent listening in the response.
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.

        :param user:
        :param recenttracks:
        :return:
        """
        pass

    def getInfo(self, user: str):
        """
        user (Optional) : The user to fetch info for. Defaults to the authenticated user.
        :param user:
        :return:
        """
        pass

    def getLovedTracks(self, user: str):
        """
        user (Required) : The user name to fetch the loved tracks for.
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.
        :param user:
        :return:
        """
        pass

    def getPersonalTags(self, user: str, tag: str, taggingtype: str):
        """
        user (Required) : The user who performed the taggings.
        tag (Required) : The tag you're interested in.
        taggingtype[artist|album|track] (Required) : The type of items which have been tagged
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.
        :param user:
        :param tag:
        :param taggingtype:
        :return:
        """
        pass

    def getRecentTracks(
        self, user: str, extended: bool, frm: datetime, to: datetime
    ):
        """
        limit (Optional) : The number of results to fetch per page. Defaults to 50. Maximum is 200.
        user (Required) : The last.fm username to fetch the recent tracks of.
        page (Optional) : The page number to fetch. Defaults to first page.
        from (Optional) : Beginning timestamp of a range - only display scrobbles after this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        extended (0|1) (Optional) : Includes extended data in each artist, and whether or not the user has loved each track
        to (Optional) : End timestamp of a range - only display scrobbles before this time, in UNIX timestamp format (integer number of seconds since 00:00:00, January 1st 1970 UTC). This must be in the UTC time zone.
        :param user:
        :param extended:
        :param frm:
        :param to:
        :return:
        """
        pass

    def getTopAlbums(self, user: str, period):
        """
        user (Required) : The user name to fetch top albums for.
        period (Optional) : overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top albums for.
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.
        :param user:
        :param period:
        :return:
        """
        pass

    def getTopArtists(self, user: str):
        """
        user (Required) : The user name to fetch top artists for.
        period (Optional) : overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top artists for.
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.
        :param user:
        :return:
        """
        pass

    def getTopTags(self, user: str):
        """
        user (Required) : The user name
        limit (Optional) : Limit the number of tags returned
        :param user:
        :return:
        """
        pass

    def getTopTracks(self, user: str):
        """
        user (Required) : The user name to fetch top tracks for.
        period (Optional) : overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top tracks for.
        limit (Optional) : The number of results to fetch per page. Defaults to 50.
        page (Optional) : The page number to fetch. Defaults to first page.
        :param user:
        :return:
        """
        pass

    def getWeeklyAlbumChart(self, user: str):
        """
        user (Required) : The last.fm username to fetch the charts of.
        from (Optional) : The date at which the chart should start from. See User.getChartsList for more.
        to (Optional) : The date at which the chart should end on. See User.getChartsList for more.
        :param user:
        :return:
        """
        pass

    def getWeeklyArtistChart(self, user: str):
        """
        user (Required) : The last.fm username to fetch the charts of.
        from (Optional) : The date at which the chart should start from. See User.getWeeklyChartList for more.
        to (Optional) : The date at which the chart should end on. See User.getWeeklyChartList for more.
        :param user:
        :return:
        """
        pass

    def getWeeklyChartList(self, user: str):
        """
        user (Required) : The last.fm username to fetch the charts list for.
        :param user:
        :return:
        """
        pass

    def getWeeklyTrackChart(self, user: str):
        """
        user (Required) : The last.fm username to fetch the charts of.
        from (Optional) : The date at which the chart should start from. See User.getWeeklyChartList for more.
        to (Optional) : The date at which the chart should end on. See User.getWeeklyChartList for more.
        :param user:
        :return:
        """
        pass
