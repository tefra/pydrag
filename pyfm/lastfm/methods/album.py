from lastfm.methods import apimethod
from lastfm.models import AlbumInfo, AlbumTopTags, AlbumTags, AlbumSearch


class Album:
    """
    Last.fm Album API interface for easy access/navigation
    """

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

    @apimethod
    def get_info(
        self, autocorrect: bool = True, user: str = None, lang: str = "en"
    ) -> AlbumInfo:
        """
        Get the metadata and tracklist for an album on Last.fm using the album name or a musicbrainz id.
        :param self:
        :param autocorrect: Transform misspelled artist names into correct artist names, returning the correct version instead.
        :param user: The username for the context of the request. If supplied, the user's playcount for this album is included in the response.
        :param lang: The language to return the biography in, expressed as an ISO 639 alpha-2 code.
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

    @apimethod
    def get_tags(self, user: str, autocorrect: bool = True) -> AlbumTags:
        """
        Get the tags applied by an individual user to an album on Last.fm. To retrieve the list of top tags applied to an album by all users use album.getTopTags.
        :param autocorrect: Transform misspelled artist names into correct artist names, returning the correct version instead.
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

    @apimethod
    def get_top_tags(self, autocorrect: bool = True) -> AlbumTopTags:
        """
        Get the top tags for an album on Last.fm, ordered by popularity.
        :param autocorrect: Transform misspelled artist names into correct artist names, returning the correct version instead.
        :returns: AlbumTopTags
        """
        self.assert_mbid_or_artist_and_album()
        return dict(
            mbid=self.mbid,
            album=self.album,
            artist=self.artist,
            autocorrect=autocorrect,
        )

    @apimethod
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
