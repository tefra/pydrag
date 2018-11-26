from typing import List, Optional, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.artist import Artist
from pydrag.lastfm.models.common import AttrModel, Image, Wiki
from pydrag.lastfm.models.tag import Tag

T = TypeVar("T", bound="Album")


@dataclass
class TrackMiniAttr(BaseModel):
    rank: int


@dataclass
class TrackMini(BaseModel):
    name: str
    url: str
    artist: Artist
    streamable: str
    duration: int
    attr: TrackMiniAttr

    def get_info(self) -> BaseModel:
        """
        Returns a proper full Album instance.

        :rtype: :class:`~pydrag.lastfm.models.album.Album`
        """
        from pydrag.lastfm.models.track import Track

        assert self.artist.name is not None
        return Track.find(artist=self.artist.name, track=self.name)


@dataclass
class Album(AttrModel):
    mbid: Optional[str] = None
    name: Optional[str] = None
    text: Optional[str] = None
    image: Optional[List[Image]] = None
    playcount: Optional[int] = None
    url: Optional[str] = None
    artist: Optional[Artist] = None
    listeners: Optional[int] = None
    tags: Optional[List[Tag]] = None
    streamable: Optional[int] = None
    tracks: Optional[List[TrackMini]] = None
    wiki: Optional[Wiki] = None

    @classmethod
    def from_dict(cls, data: dict):
        for what in ["tracks", "tags"]:
            try:
                data[what] = data[what][what[:-1]]
            except KeyError:
                pass

        if isinstance(data.get("artist"), str):
            data["artist"] = dict(name=data["artist"])
        return super().from_dict(data)

    @classmethod
    def find(
        cls,
        artist: str,
        album: str,
        user: Optional[str] = None,
        lang: str = "en",
    ) -> T:
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param album: The album name to find.
        :param artist: The album artist to find.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.lastfm.models.album.Album`
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
        :rtype: :class:`~pydrag.lastfm.models.album.Album`
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
    def search(cls, album: str, limit: int = 50, page: int = 1) -> List[T]:
        """
        Search for an album by name.Returns album matches sorted by relevance.

        :param album: The album name to search.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.album.Album`
        """

        return cls.retrieve(
            bind=Album,
            many=("albums", "album"),
            params=dict(
                method="album.search", limit=limit, page=page, album=album
            ),
        )

    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an album using a list of user supplied tags.

        :param tags: A list of user supplied tags to apply to this album. Accepts a maximum of 10 tags.
        :rtype: :class:`~pydrag.core.BaseModel`
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

        :param tag: A single user tag to remove from this album.
        :rtype: :class:`~pydrag.core.BaseModel`
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

    def get_tags(self, user: str) -> List[Tag]:
        """
        Get the tags applied by an individual user to an album on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="album.getTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> List[Tag]:
        """
        Get the top tags for an album on Last.fm, ordered by popularity.

        :rtype: :class:`list` of :class:`~pydrag.lastfm.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="album.getTopTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist,
                autocorrect=True,
            ),
        )
