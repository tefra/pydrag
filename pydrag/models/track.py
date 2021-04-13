from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from attr import dataclass

from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.common import BaseModel
from pydrag.models.common import Image
from pydrag.models.common import ListModel
from pydrag.models.common import RawResponse
from pydrag.models.common import ScrobbleTrack
from pydrag.models.common import Wiki
from pydrag.models.tag import Tag
from pydrag.services import ApiMixin


@dataclass
class Track(ApiMixin, BaseModel):
    """
    Last.FM track, chart and geo api wrapper.

    :param name: Track name/title
    :param artist: Artist name
    :param url: Last.fm profile url
    :param mbid: Musicbrainz ID
    :param image: List of images
    :param playcount: Total track playcount
    :param userplaycount: The user context total track playcount
    :param listeners: Total unique listeners
    :param duration: Track duration in seconds, should be int
    :param match: Search query match weight
    :param wiki: Track wiki information
    :param album: Track album information
    :param top_tags: Top user tags
    :param rank: Rank of the track based on the requested resource
    :param timestamp: Unix timestamp the user listened or loved this track
    :param loved: True/False if the track is one of the user's loved ones
    """

    name: str
    artist: Artist
    url: Optional[str] = None
    mbid: Optional[str] = None
    image: Optional[List[Image]] = None
    playcount: Optional[int] = None
    userplaycount: Optional[int] = None
    listeners: Optional[int] = None
    duration: Optional[int] = None
    match: Optional[float] = None
    wiki: Optional[Wiki] = None
    album: Optional[Album] = None
    top_tags: Optional[List[Tag]] = None
    loved: Optional[bool] = None
    timestamp: Optional[int] = None
    rank: Optional[int] = None

    @property
    def date(self) -> Optional[datetime]:
        """
        If the timestamp property is available return a datetime instance.

        :rtype: :class:`datetime.datetime`
        """
        return (
            None
            if self.timestamp is None
            else datetime.utcfromtimestamp(float(self.timestamp))
        )

    @classmethod
    def from_dict(cls, data: Dict):
        try:
            correction = data.pop("correction")
            data = correction.pop("track")
        except KeyError:
            pass

        if isinstance(data["artist"], str):
            data["artist"] = {"name": data["artist"]}

        data.update(
            {"name": str(data["name"]), "artist": Artist.from_dict(data["artist"])}
        )

        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "top_tags" in data:
            data["top_tags"] = list(map(Tag.from_dict, data["top_tags"]["tag"]))
        if "wiki" in data:
            data["wiki"] = Wiki.from_dict(data["wiki"])
        if "album" in data:
            data["album"] = Album.from_dict(data["album"])
        if "attr" in data:
            data.update(data.pop("attr"))
        if "date" in data:
            date = data.pop("date")
            if isinstance(date, dict) and "timestamp" not in data:
                date.pop("text")
                data.update(date)

        return super().from_dict(data)

    @classmethod
    def find(
        cls, artist: str, track: str, user: str = None, lang: str = "en"
    ) -> "Track":

        """
        Get the metadata for a track.

        :param artist: The artist name
        :param track: The track name
        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params={
                "method": "track.getInfo",
                "artist": artist,
                "track": track,
                "autocorrect": True,
                "username": user,
                "lang": lang,
            },
        )

    @classmethod
    def find_by_mbid(cls, mbid: str, user: str = None, lang: str = "en") -> "Track":
        """
        Get the metadata for a track.

        :param mbid: The musicbrainz id for the track
        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params={
                "method": "track.getInfo",
                "mbid": mbid,
                "autocorrect": True,
                "username": user,
                "lang": lang,
            },
        )

    def get_info(self, user: str = None, lang: str = "en") -> "Track":
        """
        There are many ways we end up with an incomplete instance of a track
        instance likes charts, tags etc, This is a quick method to refresh our
        object with complete data from the find methods.

        :param user: The username for the context of the request. If supplied, response
            will include the user's playcount and loved status
        :param lang: The language to return the biography in, ISO-639
        :rtype: :class:`~pydrag.models.artist.Track`
        """
        if self.mbid:
            return self.find_by_mbid(self.mbid, user, lang)
        else:
            return self.find(self.artist.name, self.name, user, lang)

    @classmethod
    def get_correction(cls, track: str, artist: str) -> "Track":
        """
        Use the last.fm corrections data to check whether the supplied track
        has a correction to a canonical track.

        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params={"method": "track.getCorrection", "artist": artist, "track": track},
        )

    @classmethod
    def search(cls, track: str, limit: int = 50, page: int = 1) -> ListModel["Track"]:
        """
        Search for an track by name. Returns track matches sorted by relevance.

        :param track: The track name.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            flatten="tracks.track",
            params={
                "method": "track.search",
                "limit": limit,
                "page": page,
                "track": track,
            },
        )

    @classmethod
    def get_top_tracks_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> ListModel["Track"]:
        """
        :param country: The country to fetch the top tracks.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            flatten="track",
            params={
                "method": "geo.getTopTracks",
                "country": country,
                "limit": limit,
                "page": page,
            },
        )

    @classmethod
    def get_top_tracks_chart(cls, limit: int = 50, page: int = 1) -> ListModel["Track"]:
        """
        Get the top tracks chart.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            flatten="track",
            params={"method": "chart.getTopTracks", "limit": limit, "page": page},
        )

    def add_tags(self, tags: List[str]) -> RawResponse:
        """
        Tag an track with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this track. Accepts a
            maximum of 10 tags.
        :type tags: :class:`list` of :class:`str`
        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={
                "method": "track.addTags",
                "track": self.name,
                "tags": ",".join(tags),
            },
        )

    def remove_tag(self, tag: str) -> RawResponse:
        """
        Remove a user's tag from an track.

        :param tag: A single user tag to remove from this track.
        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={"method": "track.removeTag", "track": self.name, "tag": tag},
        )

    def get_similar(self, limit: int = 50) -> ListModel["Track"]:
        """
        Get all the tracks similar to this track.

        :param limit: Limit the number of similar tracks returned
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            flatten="track",
            params={
                "method": "track.getSimilar",
                "mbid": self.mbid,
                "artist": self.artist.name,
                "track": self.name,
                "autocorrect": True,
                "limit": limit,
            },
        )

    def get_tags(self, user: str) -> ListModel[Tag]:
        """
        Get the tags applied by an individual user to an track on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params={
                "method": "track.getTags",
                "mbid": self.mbid,
                "artist": self.artist.name,
                "track": self.name,
                "autocorrect": True,
                "user": user,
            },
        )

    def get_top_tags(self) -> ListModel[Tag]:
        """
        Get the top tags for an track on Last.fm, ordered by popularity.

        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            flatten="tag",
            params={
                "method": "track.getTopTags",
                "mbid": self.mbid,
                "artist": self.artist.name,
                "track": self.name,
                "autocorrect": True,
            },
        )

    def love(self) -> RawResponse:
        """
        Love a track for a user profile.

        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={
                "method": "track.love",
                "artist": self.artist.name,
                "track": self.name,
            },
        )

    def unlove(self) -> RawResponse:
        """
        Unlove a track for a user profile.

        :rtype: :class:`~models.common.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params={
                "method": "track.unlove",
                "artist": self.artist.name,
                "track": self.name,
            },
        )

    @classmethod
    def scrobble_tracks(
        cls, tracks: List[ScrobbleTrack], batch_size=10
    ) -> ListModel[ScrobbleTrack]:
        """
        Split tracks into the desired batch size, with maximum size set to 50
        and send the tracks for processing, I am debating if this even belongs
        here.

        :param tracks: The tracks to scrobble
        :param batch_size: The number of tracks to submit per cycle
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.common.ScrobbleTrack`
        """

        def divide_chunks(items, n):
            for i in range(0, len(items), n):
                yield items[i : i + n]

        data: List[ScrobbleTrack] = []
        params = []
        for batch in list(divide_chunks(tracks, min(batch_size, 50))):
            res = Track._scrobble(batch)
            data += res.data
            params.append(res.params)

        result = ListModel(data)
        result.params = params
        return result

    @classmethod
    def _scrobble(cls, tracks: List[ScrobbleTrack]) -> ListModel[ScrobbleTrack]:
        """
        :param tracks: A list fo tracks to scrobble
        :type tracks: :class:`list` of :class:`~pydrag.models.common.ScrobbleTrack`
        :rtype: :class:`pydrag.models.common.ListModel` of
            :class:`~pydrag.models.common.ScrobbleTrack`
        """
        params = {"method": "track.scrobble"}
        params.update(
            {
                f"{field}[{idx}]": value
                for idx, track in enumerate(tracks)
                for field, value in track.to_api_dict().items()
            }
        )
        return cls.submit(
            bind=ScrobbleTrack,
            flatten="scrobble",
            stateful=True,
            params=params,
        )

    @classmethod
    def update_now_playing(
        cls,
        artist: str,
        track: str,
        album: str = None,
        track_number: int = None,
        context: str = None,
        duration: int = None,
        album_artist: str = None,
    ) -> ScrobbleTrack:
        """
        :param artist: The artist name
        :param track: The track name
        :param album: The album name
        :param track_number: The track number of the track on the album
        :param context: Sub-client version (not public)
        :param duration: The length of the track in seconds
        :param album_artist: The album artist
        :rtype: :class:`~models.common.RawResponse`
        """

        return cls.submit(
            bind=ScrobbleTrack,
            stateful=True,
            params={
                "method": "track.updateNowPlaying",
                "artist": artist,
                "track": track,
                "album": album,
                "trackNumber": track_number,
                "context": context,
                "duration": duration,
                "albumArtist": album_artist,
            },
        )
