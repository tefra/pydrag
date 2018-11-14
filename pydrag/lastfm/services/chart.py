from pydrag.lastfm import api
from pydrag.lastfm.models.common import ArtistList, TagInfoList, TrackList


class ChartService:
    """Last.fm Chart API interface for easy access/navigation."""

    def __init__(self, limit: int = 50, page: int = 1):
        """
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        """
        self.page = page
        self.limit = limit

    @api.operation
    def get_top_artists(self) -> ArtistList:
        """
        Get the top artists chart.

        :returns: ChartTopArtists
        """
        return dict(limit=self.limit, page=self.page)

    @api.operation
    def get_top_tracks(self) -> TrackList:
        """
        Get the top tracks chart.

        :returns: ChartTopTracks
        """
        return dict(limit=self.limit, page=self.page)

    @api.operation
    def get_top_tags(self) -> TagInfoList:
        """
        Get the top tags chart.

        :returns: ChartTopTags
        """
        return dict(limit=self.limit, page=self.page)
