from typing import List, Optional

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import Attributes, Image, Wiki
from pydrag.lastfm.models.tag import Tag


@dataclass
class Artist(BaseModel):
    """
    Last.FM track, chart and geo api client.

    :param name: Artist name/title
    :param mbid: Musicbrainz ID
    :param url: Last.fm profile url
    :param tag_count: Number of tags
    :param listeners: Total unique listeners
    :param playcount: Total artist playcount
    :param image: List of images
    :param match: Search query match weight
    :param tags: List of top tags
    :param bio: Artist bio information
    :param on_tour: Artist currently on tour flag
    :param similar: List of similar artists
    :param attr: Metadata details
    """

    name: str
    mbid: Optional[str] = None
    url: Optional[str] = None
    tag_count: Optional[int] = None
    listeners: Optional[int] = None
    playcount: Optional[int] = None
    image: Optional[List[Image]] = None
    match: Optional[float] = None
    tags: Optional[List[Tag]] = None
    bio: Optional[Wiki] = None
    on_tour: Optional[bool] = None
    similar: Optional[List["Artist"]] = None
    attr: Optional[Attributes] = None

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data.update(data.pop("stats"))
        except KeyError:
            pass

        try:
            correction = data.pop("correction")
            data = correction.pop("artist")
        except KeyError:
            pass

        if "name" not in data and "text" in data:
            data["name"] = data.pop("text")
        if "on_tour" in data:
            data["on_tour"] = True if data["on_tour"] == "1" else False
        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "tags" in data:
            data["tags"] = list(map(Tag.from_dict, data["tags"]["tag"]))
        if "bio" in data:
            data["bio"] = Wiki.from_dict(data["bio"])
        if "similar" in data and data["similar"]:
            data["similar"] = list(
                map(cls.from_dict, data["similar"]["artist"])
            )
        if "attr" in data:
            data["attr"] = Attributes.from_dict(data["attr"])

        return super(Artist, cls).from_dict(data)

    @classmethod
    def find(cls, artist: str, user: str = None, lang: str = "en") -> "Artist":
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
    def find_by_mbid(
        cls, mbid: str, user: str = None, lang: str = "en"
    ) -> "Artist":
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
    def search(
        cls, artist: str, limit: int = 50, page: int = 1
    ) -> List["Artist"]:
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
    ) -> List["Artist"]:
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
    def get_top_artists_chart(
        cls, limit: int = 50, page: int = 1
    ) -> List["Artist"]:
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

    def get_correction(self) -> "Artist":
        """
        Use the last.fm corrections data to check whether the supplied artist
        has a correction to a canonical artist.

        :rtype: :class:`~pydrag.lastfm.models.artist.Artist`
        """
        return self.retrieve(
            params=dict(method="artist.getCorrection", artist=self.name)
        )

    def get_similar(self, limit: int = 50) -> List["Artist"]:
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
