from typing import Dict
from typing import List
from typing import Optional

from attr import dataclass

from pydrag.models.common import BaseModel
from pydrag.models.common import Chart
from pydrag.models.common import ListModel
from pydrag.models.common import Wiki
from pydrag.services import ApiMixin


@dataclass
class Tag(BaseModel, ApiMixin):
    """
    Last.FM tag, chart and geo api wrapper.

    :param name: Tag name
    :param reach: NOIDEA
    :param url: Last.fm tag url
    :param taggings: Number of tagged objects
    :param count: NOIDEA
    :param total: NOIDEA
    :param wiki: Track wiki information
    """

    name: str
    reach: Optional[int] = None
    url: Optional[str] = None
    taggings: Optional[int] = None
    count: Optional[int] = None
    total: Optional[int] = None
    wiki: Optional[Wiki] = None

    @classmethod
    def from_dict(cls, data: Dict):
        if "wiki" in data:
            data["wiki"] = Wiki.from_dict(data["wiki"])
        return super().from_dict(data)

    @classmethod
    def find(cls, name: str, lang: str = None) -> "Tag":
        """
        Get the metadata for a tag.

        :param name: The tag name
        :param lang: The language to return the wiki in, ISO-639
        :rtype: :class:`~pydrag.models.tag.Tag`
        """
        return cls.retrieve(
            bind=Tag, params={"method": "tag.getInfo", "tag": name, "lang": lang}
        )

    @classmethod
    def get_top_tags(cls, limit: int = 50, page: int = 1) -> ListModel["Tag"]:
        """
        Fetches the top global tags on Last.fm, sorted by popularity Old school
        pagination on this endpoint, keep uniformity.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        return cls.retrieve(
            bind=Tag,
            flatten="tag",
            params={
                "method": "tag.getTopTags",
                "num_res": limit,
                "offset": ((page - 1) * limit),
            },
        )

    @classmethod
    def get_top_tags_chart(cls, limit: int = 50, page: int = 1) -> ListModel["Tag"]:
        """
        Get the top tags chart.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        return cls.retrieve(
            bind=Tag,
            flatten="tag",
            params={"method": "chart.getTopTags", "limit": limit, "page": page},
        )

    def get_similar(self) -> ListModel["Tag"]:
        """
        Search for tags similar to this one. Returns tags ranked by similarity,
        based on listening data.

        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params={"method": "tag.getSimilar", "tag": self.name},
        )

    def get_top_albums(self, limit: int = 50, page: int = 1) -> List:
        """
        Get the top albums tagged by this tag, ordered by tag count.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.album.Album`
        """
        from pydrag.models.album import Album

        return self.retrieve(
            bind=Album,
            flatten="album",
            params={
                "method": "tag.getTopAlbums",
                "tag": self.name,
                "limit": limit,
                "page": page,
            },
        )

    def get_top_artists(self, limit: int = 50, page: int = 1) -> List:
        """
        Get the top artists tagged by this tag, ordered by tag count.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.artist.Artist`
        """
        from pydrag.models.artist import Artist

        return self.retrieve(
            bind=Artist,
            flatten="artist",
            params={
                "method": "tag.getTopArtists",
                "tag": self.name,
                "limit": limit,
                "page": page,
            },
        )

    def get_top_tracks(self, limit: int = 50, page: int = 1) -> List:
        """
        Get the top tracks tagged by this tag, ordered by tag count.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.track.Track`
        """
        from pydrag.models.track import Track

        return self.retrieve(
            bind=Track,
            flatten="track",
            params={
                "method": "tag.getTopTracks",
                "tag": self.name,
                "limit": limit,
                "page": page,
            },
        )

    def get_weekly_chart_list(self) -> ListModel[Chart]:
        """
        Get a list of available charts for this tag, expressed as date ranges
        which can be sent to the chart services.

        :rtype: :class:`pydrag.models.common.ListModel` of :class:`~pydrag.models.common.Chart`
        """
        return self.retrieve(
            bind=Chart,
            flatten="chart",
            params={"method": "tag.getWeeklyChartList", "tag": self.name},
        )
