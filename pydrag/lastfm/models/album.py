from typing import List, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import (
    Album,
    Image,
    OpenSearch,
    RootAttributes,
    TagList,
    Tags,
    Tracks,
    Wiki,
)


@dataclass
class AlbumInfo(Album):
    artist: str = None
    listeners: int = None
    tags: Tags = None
    streamable: int = None
    tracks: Tracks = None
    wiki: Wiki = None


@dataclass
class AlbumMatches(BaseModel):
    album: List[AlbumInfo]


@dataclass
class AlbumSearch(OpenSearch):
    matches: AlbumMatches


T = TypeVar("T", bound="Album")


@dataclass
class Album(BaseModel):
    mbid: str = None
    text: str = None
    name: str = None
    title: str = None
    playcount: int = None
    url: str = None
    image: List[Image] = None
    attr: RootAttributes = None
    artist: str = None
    listeners: int = None
    tags: Tags = None
    streamable: int = None
    tracks: Tracks = None
    wiki: Wiki = None

    @classmethod
    def find(
        cls, artist: str, album: str, user: str = None, lang: str = "en"
    ) -> T:
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param album: The album name to find.
        :param artist: The album artist to find.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :returns: AlbumInfo
        """

        return cls.retrieve(
            params=dict(
                method="album.getInfo",
                album=album,
                artist=artist,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def find_by_mbid(cls, mbid: str, user: str = None, lang: str = "en") -> T:
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param mbid: The musicbrainz id for the album.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :returns: AlbumInfo
        """

        return cls.retrieve(
            params=dict(
                method="album.getInfo",
                mbid=mbid,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def search(cls, album: str, limit: int = 50, page: int = 1) -> AlbumSearch:
        """
        Search for an album by name.Returns album matches sorted by relevance.

        :param album: The album name to search.
        :param int page: The page number to fetch. Defaults to first page.
        :param int limit: The number of results to fetch per page.
        :returns: AlbumSearch
        """

        return cls.retrieve(
            bind=AlbumSearch,
            params=dict(
                method="album.search", limit=limit, page=page, album=album
            ),
        )

    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an album using a list of user supplied tags.

        :param tags: A list of user supplied tags to apply to this album.
         Accepts a maximum of 10 tags.
        :returns: BaseModel
        """

        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="album.addTags",
                arist=self.artist,
                album=self.name,
                tags=",".join(tags),
            ),
        )

    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an album.

        :param tag  : A single user tag to remove from this album.
        :returns: BaseModel
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="album.removeTag",
                album=self.name,
                artist=self.artist,
                tag=tag,
            ),
        )

    def get_tags(self, user: str) -> TagList:
        """
        Get the tags applied by an individual user to an album on Last.fm.

        :param user: The username for the context of the request.
        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="album.getTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> TagList:
        """
        Get the top tags for an album on Last.fm, ordered by popularity.

        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="album.getTopTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist,
                autocorrect=True,
            ),
        )
