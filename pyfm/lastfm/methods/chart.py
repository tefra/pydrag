from lastfm import ApiMethod
from lastfm.models import ChartTopArtists, ChartTopTracks, ChartTopTags


class Chart:
    """
    Last.fm Chart API interface for easy access/navigation
    """

    def __init__(self, limit: int = 50, page: int = 1):
        """
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        """
        self.page = page
        self.limit = limit

    @ApiMethod.fetch
    def get_top_artists(self) -> ChartTopArtists:
        """
        Get the top artists chart
        :returns: ChartTopArtists
        """
        return dict(limit=self.limit, page=self.page)

    @ApiMethod.fetch
    def get_top_tracks(self) -> ChartTopTracks:
        """
        Get the top tracks chart
        :returns: ChartTopTracks
        """
        return dict(limit=self.limit, page=self.page)

    @ApiMethod.fetch
    def get_top_tags(self) -> ChartTopTags:
        """
        Get the top tags chart
        :returns: ChartTopTags
        """
        return dict(limit=self.limit, page=self.page)
