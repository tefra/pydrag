from typing import List, Optional

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.artist import Artist
from pydrag.lastfm.models.common import AttrModel, Image, RootAttributes, Wiki
from pydrag.lastfm.models.tag import Tag


@dataclass
class TrackMiniAttr(BaseModel):
    rank: int


@dataclass
class TrackMini(BaseModel):
    name: str
    url: str
    artist: Artist
    duration: int
    attr: TrackMiniAttr

    @classmethod
    def from_dict(cls, data: dict):
        data["artist"] = Artist.from_dict(data["artist"])
        data["attr"] = TrackMiniAttr.from_dict(data["attr"])
        return super(TrackMini, cls).from_dict(data)

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
    """
    Last.FM track, chart and geo api client.

    :param name: Artist name/title
    :param mbid: Musicbrainz ID
    :param url: Last.fm profile url
    :param image: List of images
    :param text: NOIDEA
    :param playcount: Total artist playcount
    :param artist: Album artist
    :param listeners: Total unique listeners
    :param tags: List of top tags
    :param tracks: List of album tracks
    :param wiki: Album wiki information
    """

    name: Optional[str] = None
    mbid: Optional[str] = None
    url: Optional[str] = None
    image: Optional[List[Image]] = None
    text: Optional[str] = None
    playcount: Optional[int] = None
    artist: Optional[Artist] = None
    listeners: Optional[int] = None
    tags: Optional[List[Tag]] = None
    tracks: Optional[List[TrackMini]] = None
    wiki: Optional[Wiki] = None

    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data.get("artist"), str):
            data["artist"] = dict(name=data["artist"])

            data.update(
                {
                    k: str(data[k])
                    for k in ["name", "mbid", "url", "text"]
                    if k in data
                }
            )
        data.update(
            {k: int(data[k]) for k in ["playcount", "listeners"] if k in data}
        )

        if "artist" in data:
            data["artist"] = Artist.from_dict(data["artist"])
        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "tags" in data:
            data["tags"] = list(map(Tag.from_dict, data["tags"]["tag"]))
        if "tracks" in data:
            data["tracks"] = list(
                map(TrackMini.from_dict, data["tracks"]["track"])
            )
        if "wiki" in data:
            data["wiki"] = Wiki.from_dict(data["wiki"])
        if "attr" in data:
            data["attr"] = RootAttributes.from_dict(data["attr"])
        return cls(**data)

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
    def find_by_mbid(
        cls, mbid: str, user: str = None, lang: str = "en"
    ) -> "Album":
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

    def get_info(self):
        if self.mbid:
            return self.find_by_mbid(self.mbid)
        else:
            return self.find(self.artist.name, self.name)

    @classmethod
    def search(
        cls, album: str, limit: int = 50, page: int = 1
    ) -> List["Album"]:
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
