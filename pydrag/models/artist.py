from typing import Dict
from typing import List
from typing import Optional

from attr import dataclass

from pydrag.models.common import BaseModel
from pydrag.models.common import Image
from pydrag.models.common import ListModel
from pydrag.models.common import RawResponse
from pydrag.models.common import Wiki
from pydrag.models.tag import Tag
from pydrag.services import ApiMixin


@dataclass
class Artist(BaseModel, ApiMixin):
    """
    Last.FM track, chart and geo api wrapper.

    :param name: Artist name/title
    :param mbid: Musicbrainz ID
    :param url: Last.fm profile url
    :param tag_count: Number of tags
    :param listeners: Total unique listeners
    :param playcount: Total artist playcount
    :param playcount: Total user artist playcount, if user context is enabled
    :param image: List of images
    :param match: Search query match weight
    :param tags: List of top tags
    :param bio: Artist bio information
    :param on_tour: Artist currently on tour flag
    :param similar: List of similar artists
    :param rank: Rank of the artist based on the requested resource
    """

    name: str
    mbid: Optional[str] = None
    url: Optional[str] = None
    tag_count: Optional[int] = None
    listeners: Optional[int] = None
    playcount: Optional[int] = None
    userplaycount: Optional[int] = None
    image: Optional[List[Image]] = None
    match: Optional[float] = None
    tags: Optional[List[Tag]] = None
    bio: Optional[Wiki] = None
    on_tour: Optional[bool] = None
    similar: Optional[List["Artist"]] = None
    rank: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict):
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
        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "tags" in data:
            data["tags"] = list(map(Tag.from_dict, data["tags"]["tag"]))
        if "bio" in data:
            data["bio"] = Wiki.from_dict(data["bio"])
        if "similar" in data and data["similar"]:
            data["similar"] = list(map(cls.from_dict, data["similar"]["artist"]))
        if "attr" in data:
            data.update(data.pop("attr"))

        return super().from_dict(data)

    @classmethod
    def find(cls, artist: str, user: str = None, lang: str = "en") -> "Artist":
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param artist:  The artist name to retrieve.
        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.artist.Artist`
        """

        return cls.retrieve(
            bind=Artist,
            params={
                "method": "artist.getInfo",
                "artist": artist,
                "autocorrect": True,
                "username": user,
                "lang": lang,
            },
        )

    @classmethod
    def find_by_mbid(cls, mbid: str, user: str = None, lang: str = "en") -> "Artist":
        """
        Get the metadata for an artist. Includes biography, truncated at 300
        characters.

        :param mbid:  The musicbrainz id for the artist
        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.artist.Artist`
        """

        return cls.retrieve(
            bind=Artist,
            params={
                "method": "artist.getInfo",
                "mbid": mbid,
                "autocorrect": True,
                "username": user,
                "lang": lang,
            },
        )

    def get_info(self, user: str = None, lang: str = "en") -> "Artist":
        """
        There are many ways we end up with an incomplete instance of an artist
        instance likes charts, tags etc, This is a quick method to refresh our
        object with complete data from the find methods.

        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.artist.Artist`
        """
        if self.mbid:
            return self.find_by_mbid(self.mbid, user, lang)
        else:
            return self.find(self.name, user, lang)

    @classmethod
    def search(cls, artist: str, limit: int = 50, page: int = 1) -> ListModel["Artist"]:
        """
        Search for an artist by name. Returns artist matches sorted by
        relevance.

        :param artist: The artist name to search.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            flatten="artists.artist",
            params={
                "method": "artist.search",
                "limit": limit,
                "page": page,
                "artist": artist,
            },
        )

    @classmethod
    def get_top_artists_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> ListModel["Artist"]:
        """
        :param country: The country name to fetch results.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            flatten="artist",
            params={
                "method": "geo.getTopArtists",
                "country": country,
                "limit": limit,
                "page": page,
            },
        )

    @classmethod
    def get_top_artists_chart(
        cls, limit: int = 50, page: int = 1
    ) -> ListModel["Artist"]:
        """
        Get the top artists chart.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.artist.Artist`
        """
        return cls.retrieve(
            bind=Artist,
            flatten="artist",
            params={"method": "chart.getTopArtists", "limit": limit, "page": page},
        )

    def add_tags(self, tags: List[str]) -> RawResponse:
        """
        Tag an artist with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this artist.
            Accepts a maximum of 10 tags.
        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={
                "method": "artist.addTags",
                "arist": self.name,
                "tags": ",".join(tags),
            },
        )

    def remove_tag(self, tag: str) -> RawResponse:
        """
        Remove a user's tag from an artist.

        :param tag: A single user tag to remove from this artist.
        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={"method": "artist.removeTag", "arist": self.name, "tag": tag},
        )

    def get_correction(self) -> "Artist":
        """
        Use the last.fm corrections data to check whether the supplied artist
        has a correction to a canonical artist.

        :rtype: :class:`~pydrag.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            params={"method": "artist.getCorrection", "artist": self.name},
        )

    def get_similar(self, limit: int = 50) -> ListModel["Artist"]:
        """
        Get all the artists similar to this artist.

        :param limit: Limit the number of similar artists returned
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.artist.Artist`
        """
        return self.retrieve(
            bind=Artist,
            flatten="artist",
            params={
                "method": "artist.getSimilar",
                "mbid": self.mbid,
                "artist": self.name,
                "autocorrect": True,
                "limit": limit,
            },
        )

    def get_tags(self, user: str) -> ListModel[Tag]:
        """
        Get the tags applied by an individual user to an artist on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params={
                "method": "artist.getTags",
                "mbid": self.mbid,
                "artist": self.name,
                "autocorrect": True,
                "user": user,
            },
        )

    def get_top_tags(self) -> ListModel[Tag]:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params={
                "method": "artist.getTopTags",
                "mbid": self.mbid,
                "artist": self.name,
                "autocorrect": True,
            },
        )

    def get_top_tracks(self, limit: int = 50, page: int = 1) -> List:
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.

        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.track.Track`
        """
        from pydrag.models.track import Track

        return self.retrieve(
            bind=Track,
            flatten="track",
            params={
                "method": "artist.getTopTracks",
                "mbid": self.mbid,
                "artist": self.name,
                "autocorrect": True,
                "limit": limit,
                "page": page,
            },
        )
