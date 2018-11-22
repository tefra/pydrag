from typing import List, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import (
    Artist,
    ArtistList,
    Artists,
    Attributes,
    AttrModel,
    Image,
    OpenSearch,
    Query,
    TagList,
    Tags,
    TrackList,
    Wiki,
)


@dataclass
class CorrectionArtist(AttrModel):
    artist: Artist


@dataclass
class ArtistCorrection(BaseModel):
    correction: CorrectionArtist


@dataclass
class ArtistMatches(BaseModel):
    artist: List[Artist]


@dataclass
class ArtistSearch(OpenSearch):
    matches: ArtistMatches
    query: Query


T = TypeVar("T", bound="Artist")


@dataclass
class Artist(BaseModel):
    mbid: str = None
    name: str = None
    url: str = None
    tag_count: int = None
    listeners: int = None
    playcount: int = None
    streamable: str = None
    image: List[Image] = None
    match: str = None
    attr: Attributes = None
    tags: Tags = None
    bio: Wiki = None
    on_tour: int = None
    stats: Artist = None
    similar: Artists = None

    @classmethod
    def find(cls, artist: str, user: str = None, lang: str = "en") -> T:
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param artist:  The artist name to retrieve.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :returns: ArtistInfo
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
        :returns: ArtistInfo
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
    def search(
        cls, artist: str, limit: int = 50, page: int = 1
    ) -> ArtistSearch:
        """
        Search for an artist by name. Returns artist matches sorted by
        relevance.

        :param artist: The artist name to search.
        :param int page: The page number to fetch.
        :param int limit: The number of results to fetch per page.
        :returns: ArtistSearch
        """
        return cls.retrieve(
            bind=ArtistSearch,
            params=dict(
                method="artist.search", limit=limit, page=page, artist=artist
            ),
        )

    @classmethod
    def get_top_artists_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> ArtistList:
        """
        :param country: The country name to fetch results.
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch.
        :returns: TrackList
        """
        return cls.retrieve(
            bind=ArtistList,
            params=dict(
                method="geo.getTopArtists",
                country=country,
                limit=limit,
                page=page,
            ),
        )

    @classmethod
    def get_top_artists_chart(
        cls, limit: int = 50, page: int = 1
    ) -> ArtistList:
        """
        Get the top artists chart.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: ArtistList
        """
        return cls.retrieve(
            bind=ArtistList,
            params=dict(method="chart.getTopArtists", limit=limit, page=page),
        )

    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an artist with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this artist.
        Accepts a maximum of 10 tags.
        :returns: BaseModel
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
        :returns: BaseModel
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

        :returns: ArtistCorrection
        """
        return self.retrieve(
            bind=ArtistCorrection,
            params=dict(method="artist.getCorrection", artist=self.name),
        )

    def get_similar(self, limit: int = 50) -> ArtistList:
        """
        Get all the artists similar to this artist.

        :param int limit: Limit the number of similar artists returned
        :returns: ArtistList
        """
        return self.retrieve(
            bind=ArtistList,
            params=dict(
                method="artist.getSimilar",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                limit=limit,
            ),
        )

    def get_tags(self, user: str) -> TagList:
        """
        Get the tags applied by an individual user to an artist on Last.fm.

        :param user: The username for the context of the request.
        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="artist.getTags",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> TagList:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="artist.getTopTags",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
            ),
        )

    def get_top_tracks(self, limit: int = 50, page: int = 1) -> TrackList:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :param int page: The page number to fetch.
        :param int limit: The number of results to fetch per page.
        :returns: ArtistTopTracks
        """
        return self.retrieve(
            bind=TrackList,
            params=dict(
                method="artist.getTopTracks",
                mbid=self.mbid,
                artist=self.name,
                autocorrect=True,
                limit=limit,
                page=page,
            ),
        )
