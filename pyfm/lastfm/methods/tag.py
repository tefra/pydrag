from lastfm.methods import apimethod
from lastfm.models import (
    TagInfo,
    TagTopAlbums,
    TagTopArtists,
    TagTopTags,
    TagTopTracks,
    TagWeeklyChartList,
)


class Tag:
    """
    Last.fm Tag API interface for easy access/navigation
    """

    def __init__(self, tag: str = None):
        """
        :param str tag: The tag name
        """
        self.tag = tag

    @apimethod
    def get_info(self, lang: str = None) -> TagInfo:
        """
        Get the metadata for a tag
        :param lang: The language to return the wiki in, expressed as an ISO 639 alpha-2 code.
        :return: TagInfo
        """
        assert self.tag is not None
        return dict(tag=self.tag, lang=lang)

    @apimethod
    def get_similar(self) -> TagInfo:
        """
        Search for tags similar to this one. Returns tags ranked by similarity, based on listening data.
        :param lang: The language to return the wiki in, expressed as an ISO 639 alpha-2 code.
        :return: TagInfo
        """
        assert self.tag is not None
        return dict(tag=self.tag)

    @apimethod
    def get_top_albums(self, limit: int = 50, page: int = 1) -> TagTopAlbums:
        """
        Get the top albums tagged by this tag, ordered by tag count.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: TagTopAlbums
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @apimethod
    def get_top_artists(self, limit: int = 50, page: int = 1) -> TagTopArtists:
        """
        Get the top artists tagged by this tag, ordered by tag count.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: TagTopArtists
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @apimethod
    def get_top_tracks(self, limit: int = 50, page: int = 1) -> TagTopTracks:
        """
        Get the top tracks tagged by this tag, ordered by tag count.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: TagTopArtists
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @apimethod
    def get_top_tags(self, limit: int = 50, page: int = 1) -> TagTopTags:
        """
        Fetches the top global tags on Last.fm, sorted by popularity (number of times used)
        Old school pagination on this endpoint, keep uniformity
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: TagTopTags
        """
        return dict(num_res=limit, offset=(page - 1) * page)

    @apimethod
    def get_weekly_chart_list(self) -> TagWeeklyChartList:
        """
        Get a list of available charts for this tag, expressed as date ranges which can be sent to the chart services.
        :return: TagWeeklyChartList
        """
        assert self.tag is not None
        return dict(tag=self.tag)
