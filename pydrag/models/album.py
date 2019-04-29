from typing import Dict, List, Optional

from attr import dataclass

from pydrag.models.artist import Artist
from pydrag.models.common import BaseModel, Image, ListModel, RawResponse, Wiki
from pydrag.models.tag import Tag
from pydrag.services import ApiMixin


@dataclass
class Album(BaseModel, ApiMixin):
    """
    Last.FM track, chart and geo api wrapper.

    :param name: Artist name/title
    :param mbid: Musicbrainz ID
    :param url: Last.fm profile url
    :param image: List of images
    :param playcount: Total artist playcount
    :param artist: Album artist
    :param listeners: Total unique listeners
    :param tags: List of top tags
    :param tracks: List of album tracks
    :param wiki: Album wiki information
    :param rank: Rank of the album based on the requested resource
    """

    name: str
    mbid: Optional[str] = None
    url: Optional[str] = None
    image: Optional[List[Image]] = None
    playcount: Optional[int] = None
    artist: Optional[Artist] = None
    listeners: Optional[int] = None
    tags: Optional[List[Tag]] = None
    tracks: Optional[List["Track"]] = None  # type: ignore
    wiki: Optional[Wiki] = None
    rank: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict):
        if isinstance(data.get("artist"), str):
            data["artist"] = dict(name=data["artist"])

        if "name" not in data and "text" in data:
            data["name"] = data.pop("text")
        if "artist" in data:
            data["artist"] = Artist.from_dict(data["artist"])
        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "tags" in data:
            data["tags"] = list(map(Tag.from_dict, data["tags"]["tag"]))
        if "tracks" in data:
            from pydrag.models.track import Track

            data["tracks"] = list(
                map(Track.from_dict, data["tracks"]["track"])
            )
        if "wiki" in data:
            data["wiki"] = Wiki.from_dict(data["wiki"])
        if "attr" in data:
            data.update(data.pop("attr"))

        return super(Album, cls).from_dict(data)

    @classmethod
    def find(
        cls,
        artist: str,
        album: str,
        user: Optional[str] = None,
        lang: str = "en",
    ) -> "Album":
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param album: The album name to find.
        :param artist: The album artist to find.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.album.Album`
        """

        return cls.retrieve(
            bind=Album,
            params=dict(
                method="album.getInfo",
                album=album,
                artist=artist,
                autocorrect=True,
                username=user,
                lang=lang,
            ),
        )

    @classmethod
    def find_by_mbid(
        cls, mbid: str, user: str = None, lang: str = "en"
    ) -> "Album":
        """
        Get the metadata and tracklist for an album on Last.fm.

        :param mbid: The musicbrainz id for the album.
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this album
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.album.Album`
        """

        return cls.retrieve(
            bind=Album,
            params=dict(
                method="album.getInfo",
                mbid=mbid,
                autocorrect=True,
                username=user,
                lang=lang,
            ),
        )

    def get_info(self, user: str = None, lang: str = "en") -> "Album":
        """
        There are many ways we end up with an incomplete instance of an album
        instance likes charts, tags etc, This is a quick method to refresh our
        object with complete data from the find methods.

        :param user: The username for the context of the request. If supplied, response will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.artist.Album`
        """
        if self.mbid:
            return self.find_by_mbid(self.mbid, user, lang)
        else:
            if self.artist is None:
                raise ValueError("Missing artist name!")

            return self.find(self.artist.name, self.name, user, lang)

    @classmethod
    def search(
        cls, album: str, limit: int = 50, page: int = 1
    ) -> ListModel["Album"]:
        """
        Search for an album by name.Returns album matches sorted by relevance.

        :param album: The album name to search.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.album.Album`
        """

        return cls.retrieve(
            bind=Album,
            flatten="albums.album",
            params=dict(
                method="album.search", limit=limit, page=page, album=album
            ),
        )

    def add_tags(self, tags: List[str]) -> RawResponse:
        """
        Tag an album using a list of user supplied tags.

        :param tags: A list of user supplied tags to apply to this album. Accepts a maximum of 10 tags.
        :rtype: :class:`~models.common.RawResponse`
        """
        if self.artist is None:
            raise ValueError("Missing artist name!")

        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(
                method="album.addTags",
                arist=self.artist.name,
                album=self.name,
                tags=",".join(tags),
            ),
        )

    def remove_tag(self, tag: str) -> RawResponse:
        """
        Remove a user's tag from an album.

        :param tag: A single user tag to remove from this album.
        :rtype: :class:`~models.common.RawResponse`
        """
        if self.artist is None:
            raise ValueError("Missing artist name!")

        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(
                method="album.removeTag",
                album=self.name,
                artist=self.artist.name,
                tag=tag,
            ),
        )

    def get_tags(self, user: str) -> ListModel[Tag]:
        """
        Get the tags applied by an individual user to an album on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        if self.artist is None:
            raise ValueError("Missing artist name!")

        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params=dict(
                method="album.getTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist.name,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> ListModel[Tag]:
        """
        Get the top tags for an album on Last.fm, ordered by popularity.

        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        if self.artist is None:
            raise ValueError("Missing artist name!")

        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params=dict(
                method="album.getTopTags",
                mbid=self.mbid,
                album=self.name,
                artist=self.artist.name,
                autocorrect=True,
            ),
        )
