from typing import List, TypeVar

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

        :returns: Track
        """
        from pydrag.lastfm.models.track import Track

        return Track.find(artist=self.artist.name, track=self.name)


@dataclass
class Album(AttrModel):
    mbid: str = None
    name: str = None
    text: str = None
    image: List[Image] = None
    playcount: int = None
    url: str = None
    artist: Artist = None
    listeners: int = None
    tags: List[Tag] = None
    streamable: int = None
    tracks: List[TrackMini] = None
    wiki: Wiki = None

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
        cls, artist: str, album: str, user: str = None, lang: str = "en"
    ) -> T:
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param album: The album name to find.
        :param artist: The album artist to find.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :returns: Album
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
        :returns: Album
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
        :param int page: The page number to fetch.
        :param int limit: The number of results to fetch per page.
        :returns: List[Album]
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

    def get_tags(self, user: str) -> List[Tag]:
        """
        Get the tags applied by an individual user to an album on Last.fm.

        :param user: The username for the context of the request.
        :returns: List[Tag]
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

        :returns: List[Tag]
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
