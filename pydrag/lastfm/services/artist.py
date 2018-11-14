from typing import List

from pydrag.core import BaseModel
from pydrag.lastfm import POST, api
from pydrag.lastfm.models.artist import (
    ArtistCorrection,
    ArtistInfo,
    ArtistSearch,
    ArtistSimilar,
    ArtistTags,
    ArtistTopTags,
    ArtistTopTracks,
)


class ArtistService:
    """Last.fm Artist API interface for easy access/navigation."""

    def __init__(self, artist: str = None, mbid: str = None):
        """
        :param artist: The artist name
        :param mbid: The musicbrainz id for the artist
        """
        self.mbid = mbid
        self.artist = artist

    @api.operation(method=POST, stateful=True)
    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an artist with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this artist.
        Accepts a maximum of 10 tags.
        :returns: BaseModel
        """
        assert self.artist is not None
        return dict(artist=self.artist, tags=",".join(tags))

    @api.operation(method=POST, stateful=True)
    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an artist.

        :param tag: A single user tag to remove from this artist.
        :returns: BaseModel
        """
        assert self.artist is not None
        return dict(artist=self.artist, tag=tag)

    @api.operation
    def get_info(
        self, autocorrect: bool = True, user: str = None, lang: str = "en"
    ) -> ArtistInfo:
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param autocorrect: If enabled auto correct misspelled names
        :param user: The username for the context of the request.
        If supplied, response will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :returns: ArtistInfo
        """

        self.assert_mbid_or_artist()
        return dict(
            mbid=self.mbid,
            artist=self.artist,
            autocorrect=autocorrect,
            username=user,
            lang=lang,
        )

    @api.operation
    def get_correction(self) -> ArtistCorrection:
        """
        Use the last.fm corrections data to check whether the supplied artist
        has a correction to a canonical artist.

        :returns: ArtistCorrection
        """
        assert self.artist is not None
        return dict(artist=self.artist)

    @api.operation
    def get_similar(
        self, autocorrect: bool = True, limit: int = 50
    ) -> ArtistSimilar:
        """
        Get all the artists similar to this artist.

        :param autocorrect: If enabled auto correct misspelled names
        :param int limit: Limit the number of similar artists returned
        :returns: ArtistSimilar
        """
        self.assert_mbid_or_artist()
        return dict(
            mbid=self.mbid,
            artist=self.artist,
            autocorrect=autocorrect,
            limit=limit,
        )

    @api.operation
    def get_tags(self, user: str, autocorrect: bool = True) -> ArtistTags:
        """
        Get the tags applied by an individual user to an artist on Last.fm.

        :param user: The username for the context of the request.
        :param autocorrect: If enabled auto correct misspelled names
        :returns: ArtistTags
        """
        self.assert_mbid_or_artist()
        return dict(
            mbid=self.mbid,
            artist=self.artist,
            autocorrect=autocorrect,
            user=user,
        )

    @api.operation
    def get_top_tags(self, autocorrect: bool = True) -> ArtistTopTags:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :param autocorrect: If enabled auto correct misspelled names
        :returns: ArtistTopTags
        """
        self.assert_mbid_or_artist()
        return dict(
            mbid=self.mbid, artist=self.artist, autocorrect=autocorrect
        )

    @api.operation
    def get_top_tracks(
        self, autocorrect: bool = True, limit: int = 50, page: int = 1
    ) -> ArtistTopTracks:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :param autocorrect: If enabled auto correct misspelled names
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: ArtistTopTracks
        """
        self.assert_mbid_or_artist()
        return dict(
            mbid=self.mbid,
            artist=self.artist,
            autocorrect=autocorrect,
            limit=limit,
            page=page,
        )

    @api.operation
    def search(self, limit: int = 50, page: int = 1) -> ArtistSearch:
        """
        Search for an artist by name. Returns artist matches sorted by
        relevance.

        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: ArtistSearch
        """
        assert self.artist is not None
        return dict(limit=limit, page=page, artist=self.artist)

    def assert_mbid_or_artist(self):
        assert self.mbid is not None or self.artist is not None
