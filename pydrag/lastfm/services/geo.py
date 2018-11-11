from pydrag.lastfm import api
from pydrag.lastfm.models import GeoTopArtists, GeoTopTracks


class GeoService:
    """Last.fm Geo API interface for easy access/navigation."""

    def __init__(self, country: str):
        """
        :param str country:  A country name, as defined by the ISO 3166-1
        """
        self.country = country

    @api.operation
    def get_top_artists(self, limit: int = 50, page: int = 1) -> GeoTopArtists:
        """
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: GeoTopArtists
        """
        return dict(country=self.country, limit=limit, page=page)

    @api.operation
    def get_top_tracks(self, limit: int = 50, page: int = 1) -> GeoTopTracks:
        """
        :param limit: The number of results to fetch per page. Defaults to 50.
        :param page: The page number to fetch. Defaults to first page.
        :returns: GeoTopArtists
        """
        return dict(country=self.country, limit=limit, page=page)
