from pydrag.lastfm import api
from pydrag.lastfm.models.common import (
    AlbumList,
    ArtistList,
    ChartList,
    TagInfo,
    TagInfoList,
    TrackList,
)


class TagService:
    """Last.fm Tag API interface for easy access/navigation."""

    def __init__(self, tag: str = None):
        """
        :param str tag: The tag name
        """
        self.tag = tag

    @api.operation()
    def get_info(self, lang: str = None) -> TagInfo:
        """
        Get the metadata for a tag.

        :param lang: The language to return the wiki in, ISO-639
        :return: TagInfo
        """
        assert self.tag is not None
        return dict(tag=self.tag, lang=lang)

    @api.operation
    def get_similar(self) -> TagInfoList:
        """
        Search for tags similar to this one. Returns tags ranked by similarity,
        based on listening data.

        :return: TagInfo
        """
        assert self.tag is not None
        return dict(tag=self.tag)

    @api.operation
    def get_top_albums(self, limit: int = 50, page: int = 1) -> AlbumList:
        """
        Get the top albums tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TagTopAlbums
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @api.operation
    def get_top_artists(self, limit: int = 50, page: int = 1) -> ArtistList:
        """
        Get the top artists tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: ArtistList
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @api.operation
    def get_top_tracks(self, limit: int = 50, page: int = 1) -> TrackList:
        """
        Get the top tracks tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TagTopArtists
        """
        assert self.tag is not None
        return dict(tag=self.tag, limit=limit, page=page)

    @api.operation
    def get_top_tags(self, limit: int = 50, page: int = 1) -> TagInfoList:
        """
        Fetches the top global tags on Last.fm, sorted by popularity Old school
        pagination on this endpoint, keep uniformity.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TagTopTags
        """
        return dict(num_res=limit, offset=((page - 1) * limit))

    @api.operation
    def get_weekly_chart_list(self) -> ChartList:
        """
        Get a list of available charts for this tag, expressed as date ranges
        which can be sent to the chart services.

        :return: TagWeeklyChartList
        """
        assert self.tag is not None
        return dict(tag=self.tag)
