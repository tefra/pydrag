from pydrag.lastfm import api
from pydrag.lastfm.models.common import ArtistList, TrackList


class GeoService:
    """Last.fm Geo API interface for easy access/navigation."""

    def __init__(self, country: str):
        """
        :param str country:  A country name, as defined by the ISO 3166-1
        """
        self.country = country

    @api.operation
    def get_top_artists(self, limit: int = 50, page: int = 1) -> ArtistList:
        """
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: GeoTopArtists
        """
        return dict(country=self.country, limit=limit, page=page)

    @api.operation
    def get_top_tracks(self, limit: int = 50, page: int = 1) -> TrackList:
        """
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: GeoTopArtists
        """
        return dict(country=self.country, limit=limit, page=page)
