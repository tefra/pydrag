from typing import List

from pydrag.lastfm import POST, api
from pydrag.lastfm.models import (
    AlbumInfo,
    AlbumSearch,
    AlbumTags,
    AlbumTopTags,
    BaseModel,
)


class AlbumService:
    """Last.fm Album API interface for easy access/navigation."""

    def __init__(
        self, artist: str = None, album: str = None, mbid: str = None
    ):
        """
        :param artist: The artist name
        :param album: The album name
        :param mbid: The musicbrainz id for the album
        """
        self.mbid = mbid
        self.album = album
        self.artist = artist

    @api.operation(method=POST, stateful=True)
    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an album using a list of user supplied tags.

        :param tags: A list of user supplied tags to apply to this album.
         Accepts a maximum of 10 tags.
        :returns: BaseModel
        """
        assert self.artist is not None and self.album is not None
        return dict(album=self.album, artist=self.artist, tags=",".join(tags))

    @api.operation(method=POST, stateful=True)
    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an album.

        :param tag  : A single user tag to remove from this album.
        :returns: BaseModel
        """
        assert self.artist is not None and self.album is not None
        return dict(album=self.album, artist=self.artist, tag=tag)

    @api.operation
    def get_info(
        self, autocorrect: bool = True, user: str = None, lang: str = "en"
    ) -> AlbumInfo:
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param self:
        :param autocorrect: If enabled auto correct misspelled names
        :param user: The username for the context of the request.
        If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :returns: AlbumInfo
        """

        self.assert_mbid_or_artist_and_album()
        return dict(
            mbid=self.mbid,
            album=self.album,
            artist=self.artist,
            autocorrect=autocorrect,
            username=user,
            lang=lang,
        )

    @api.operation
    def get_tags(self, user: str, autocorrect: bool = True) -> AlbumTags:
        """
        Get the tags applied by an individual user to an album on Last.fm.

        :param user: The username for the context of the request.
        :param autocorrect: If enabled auto correct misspelled names
        :returns: AlbumTopTags
        """
        self.assert_mbid_or_artist_and_album()
        return dict(
            mbid=self.mbid,
            album=self.album,
            artist=self.artist,
            autocorrect=autocorrect,
            user=user,
        )

    @api.operation
    def get_top_tags(self, autocorrect: bool = True) -> AlbumTopTags:
        """
        Get the top tags for an album on Last.fm, ordered by popularity.

        :param autocorrect: If enabled auto correct misspelled names
        :returns: AlbumTopTags
        """
        self.assert_mbid_or_artist_and_album()
        return dict(
            mbid=self.mbid,
            album=self.album,
            artist=self.artist,
            autocorrect=autocorrect,
        )

    @api.operation
    def search(self, limit: int = 50, page: int = 1) -> AlbumSearch:
        """
        Search for an album by name.Returns album matches sorted by relevance.

        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :returns: AlbumSearch
        """
        assert self.album is not None

        return dict(limit=limit, page=page, album=self.album)

    def assert_mbid_or_artist_and_album(self):
        assert self.mbid is not None or (
            self.artist is not None and self.album is not None
        )
