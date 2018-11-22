from typing import TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import (
    AlbumList,
    ArtistList,
    ChartList,
    TagInfoList,
    TrackList,
    Wiki,
)

T = TypeVar("T", bound="Tag")


@dataclass
class Tag(BaseModel):
    name: str
    reach: int = None
    url: str = None
    taggings: int = None
    streamable: int = None
    count: int = None
    total: int = None
    wiki: Wiki = None

    @classmethod
    def find(cls, name: str, lang: str = None) -> T:
        """
        Get the metadata for a tag.

        :param lang: The language to return the wiki in, ISO-639
        :return: TagInfo
        """
        return cls.retrieve(
            params=dict(method="tag.getInfo", tag=name, lang=lang)
        )

    @classmethod
    def get_top_tags(cls, limit: int = 50, page: int = 1) -> TagInfoList:
        """
        Fetches the top global tags on Last.fm, sorted by popularity Old school
        pagination on this endpoint, keep uniformity.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch.
        :returns: TagTopTags
        """
        return cls.retrieve(
            bind=TagInfoList,
            params=dict(
                method="tag.getTopTags",
                num_res=limit,
                offset=((page - 1) * limit),
            ),
        )

    def get_similar(self) -> TagInfoList:
        """
        Search for tags similar to this one. Returns tags ranked by similarity,
        based on listening data.

        :return: TagInfo
        """
        return self.retrieve(
            bind=TagInfoList,
            params=dict(method="tag.getSimilar", tag=self.name),
        )

    def get_top_albums(self, limit: int = 50, page: int = 1) -> AlbumList:
        """
        Get the top albums tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch.
        :returns: TagTopAlbums
        """
        return self.retrieve(
            bind=AlbumList,
            params=dict(
                method="tag.getTopAlbums",
                tag=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_top_artists(self, limit: int = 50, page: int = 1) -> ArtistList:
        """
        Get the top artists tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch.
        :returns: ArtistList
        """
        return self.retrieve(
            bind=ArtistList,
            params=dict(
                method="tag.getTopArtists",
                tag=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_top_tracks(self, limit: int = 50, page: int = 1) -> TrackList:
        """
        Get the top tracks tagged by this tag, ordered by tag count.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch.
        :returns: TagTopArtists
        """
        return self.retrieve(
            bind=TrackList,
            params=dict(
                method="tag.getTopTracks",
                tag=self.name,
                limit=limit,
                page=page,
            ),
        )

    def get_weekly_chart_list(self) -> ChartList:
        """
        Get a list of available charts for this tag, expressed as date ranges
        which can be sent to the chart services.

        :return: TagWeeklyChartList
        """
        return self.retrieve(
            bind=ChartList,
            params=dict(method="tag.getWeeklyChartList", tag=self.name),
        )
