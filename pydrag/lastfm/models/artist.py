from typing import List, Optional, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import Image, RootAttributes, Wiki
from pydrag.lastfm.models.tag import Tag


@dataclass
class ArtistMini(BaseModel):
    name: str
    url: str
    mbid: Optional[str] = None
    image: Optional[List[Image]] = None


@dataclass
class CorrectionArtistAttr(BaseModel):
    index: int


@dataclass
class CorrectionArtist(BaseModel):
    artist: ArtistMini
    attr: CorrectionArtistAttr


@dataclass
class ArtistCorrection(BaseModel):
    correction: CorrectionArtist


T = TypeVar("T", bound="Artist")


@dataclass
class Artist(BaseModel):
    name: Optional[str] = None
    mbid: Optional[str] = None
    url: Optional[str] = None
    tag_count: Optional[int] = None
    listeners: Optional[int] = None
    playcount: Optional[int] = None
    streamable: Optional[str] = None
    image: Optional[List[Image]] = None
    match: Optional[str] = None
    attr: Optional[RootAttributes] = None
    tags: Optional[List[Tag]] = None
    bio: Optional[Wiki] = None
    on_tour: Optional[int] = None
    similar: Optional[List[ArtistMini]] = None
    text: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data["tags"] = data["tags"]["tag"]
        except KeyError:
            pass
        try:
            data["similar"] = data["similar"]["artist"]
        except KeyError:
            pass
        try:
            data.update(data.pop("stats"))
        except KeyError:
            pass
        return super().from_dict(data)

    @classmethod
    def find(cls, artist: str, user: str = None, lang: str = "en") -> T:
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param artist:  The artist name to retrieve.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.lastfm.models.artist.Artist`
        """

        return cls.retrieve(
            params=dict(
                method="artist.getInfo",
                artist=artist,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def find_by_mbid(cls, mbid: str, user: str = None, lang: str = "en") -> T:
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param mbid:  The musicbrainz id for the artist
        :param user: The username for the context of the request. If supplied, response will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.lastfm.models.artist.Artist`
        """

        return cls.retrieve(
            params=dict(
                method="artist.getInfo",
                mbid=mbid,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def search(cls, artist: str, limit: int = 50, page: int = 1) -> List[T]:
        """
        Search for an artist by name. Returns artist matches sorted by
        relevance.

        :param artist: The artist name to search.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            many=("artists", "artist"),
            params=dict(
                method="artist.search", limit=limit, page=page, artist=artist
            ),
        )

    @classmethod
    def get_top_artists_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> List[T]:
        """
        :param country: The country name to fetch results.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            many="artist",
            params=dict(
                method="geo.getTopArtists",
                country=country,
                limit=limit,
                page=page,
            ),
        )

    @classmethod
    def get_top_artists_chart(cls, limit: int = 50, page: int = 1) -> List[T]:
        """
        Get the top artists chart.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            many="artist",
            params=dict(method="chart.getTopArtists", limit=limit, page=page),
        )

    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an artist with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this artist. Accepts a maximum of 10 tags.
        :rtype: :class:`~pydrag.core.BaseModel`
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="artist.addTags", arist=self.name, tags=",".join(tags)
            ),
        )

    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an artist.

        :param tag: A single user tag to remove from this artist.
        :rtype: :class:`~pydrag.core.BaseModel`
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(method="artist.removeTag", arist=self.name, tag=tag),
        )

    def get_correction(self) -> ArtistCorrection:
        """
        Use the last.fm corrections data to check whether the supplied artist
        has a correction to a canonical artist.

        :rtype: :class:`~pydrag.lastfm.models.artist.ArtistCorrection`
        """
        return self.retrieve(
            bind=ArtistCorrection,
            params=dict(method="artist.getCorrection", artist=self.name),
        )

    def get_similar(self, limit: int = 50) -> List[T]:
        """
        Get all the artists similar to this artist.

        :param limit: Limit the number of similar artists returned
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            many="artist",
            params=dict(
                method="artist.getSimilar",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                limit=limit,
            ),
        )

    def get_tags(self, user: str) -> List[Tag]:
        """
        Get the tags applied by an individual user to an artist on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="artist.getTags",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> List[Tag]:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="artist.getTopTags",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
            ),
        )

    def get_top_tracks(self, limit: int = 50, page: int = 1) -> List:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.track.Track`
        """
        from pydrag.lastfm.models.track import Track

        return self.retrieve(
            bind=Track,
            many="track",
            params=dict(
                method="artist.getTopTracks",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                limit=limit,
                page=page,
            ),
        )
