from typing import List, Optional

from attr import dataclass

from pydrag.core import ApiMixin, BaseModel, ListModel, RawResponse
from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.common import Attributes, Date, Image, Wiki
from pydrag.models.tag import Tag


@dataclass
class ScrobbleTrack(BaseModel):
    artist: str
    track: str
    track_number: Optional[str] = None
    album: Optional[str] = None
    album_artist: Optional[str] = None
    duration: Optional[int] = None
    mbid: Optional[str] = None
    timestamp: Optional[int] = None
    context: Optional[str] = None
    stream_id: Optional[str] = None
    chosen_by_user: Optional[bool] = None
    ignored_message: Optional[str] = None

    def to_dict(self):
        return super(ScrobbleTrack, self).to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        data.update(
            {
                k: data[k]["text"]
                if data.get(k, {}).get("text", "") != ""
                else None
                for k in [
                    "album",
                    "artist",
                    "track",
                    "ignored_message",
                    "album_artist",
                ]
            }
        )
        return super(ScrobbleTrack, cls).from_dict(data)


@dataclass
class Track(ApiMixin, BaseModel):
    """
    Last.FM track, chart and geo api client.

    :param name: Track name/title
    :param artist: Artist name
    :param url: Last.fm profile url
    :param mbid: Musicbrainz ID
    :param image: List of images
    :param playcount: Total track playcount
    :param listeners: Total unique listeners
    :param duration: Track duration in seconds, should be int
    :param match: Search query match weight
    :param wiki: Track wiki information
    :param album: Track album information
    :param top_tags: Top user tags
    :param date: Date the user listened or loved this track
    :param loved: True/False if the track is one of the user's loved ones
    :param attr: Metadata details
    """

    name: str
    artist: Artist
    url: Optional[str] = None
    mbid: Optional[str] = None
    image: Optional[List[Image]] = None
    playcount: Optional[int] = None
    listeners: Optional[int] = None
    duration: Optional[int] = None
    match: Optional[float] = None
    wiki: Optional[Wiki] = None
    album: Optional[Album] = None
    top_tags: Optional[List[Tag]] = None
    date: Optional[Date] = None
    loved: Optional[int] = None
    attr: Optional[Attributes] = None

    @classmethod
    def from_dict(cls, data: dict):
        try:
            if isinstance(data["album"]["artist"], str):
                data["album"]["artist"] = dict(name=data["album"]["artist"])
        except KeyError:
            pass

        try:
            correction = data.pop("correction")
            data = correction.pop("track")
        except KeyError:
            pass

        if isinstance(data["artist"], str):
            data["artist"] = dict(name=data["artist"])

        data.update(
            dict(
                name=str(data["name"]), artist=Artist.from_dict(data["artist"])
            )
        )

        if data.get("duration") == "FIXME":
            data["duration"] = 0
        if "loved" in data:
            data["loved"] = True if data["loved"] == "1" else False
        if "image" in data:
            data["image"] = list(map(Image.from_dict, data["image"]))
        if "top_tags" in data:
            data["top_tags"] = list(
                map(Tag.from_dict, data["top_tags"]["tag"])
            )
        if "match" in data:
            data["match"] = float(data["match"])
        if "wiki" in data:
            data["wiki"] = Wiki.from_dict(data["wiki"])
        if "album" in data:
            data["album"] = Album.from_dict(data["album"])
        if "attr" in data:
            data["attr"] = Attributes.from_dict(data["attr"])
        if "date" in data:
            data["date"] = Date.from_dict(data["date"])

        return super(Track, cls).from_dict(data)

    @classmethod
    def find(
        cls, artist: str, track: str, user: str = None, lang: str = "en"
    ) -> "Track":

        """
        Get the metadata for a track.

        :param artist: The artist name
        :param track: The track name
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params=dict(
                method="track.getInfo",
                artist=artist,
                track=track,
                autocorrect=True,
                username=user,
                lang=lang,
            ),
        )

    @classmethod
    def find_by_mbid(
        cls, mbid: str, user: str = None, lang: str = "en"
    ) -> "Track":
        """
        Get the metadata for a track.

        :param mbid: The musicbrainz id for the track
        :param user: The username for the context of the request. If supplied, response will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params=dict(
                method="track.getInfo",
                mbid=mbid,
                autocorrect=True,
                username=user,
                lang=lang,
            ),
        )

    @classmethod
    def get_correction(cls, track: str, artist: str) -> "Track":
        """
        Use the last.fm corrections data to check whether the supplied track
        has a correction to a canonical track.

        :rtype: :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            params=dict(
                method="track.getCorrection", artist=artist, track=track
            ),
        )

    @classmethod
    def search(
        cls, track: str, limit: int = 50, page: int = 1
    ) -> ListModel["Track"]:
        """
        Search for an track by name. Returns track matches sorted by relevance.

        :param track: The track name.
        :param page: The page number to fetch.
        :param limit: The number of results to fetch per page.
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            many="tracks.track",
            params=dict(
                method="track.search", limit=limit, page=page, track=track
            ),
        )

    @classmethod
    def get_top_tracks_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> ListModel["Track"]:
        """
        :param country: The country to fetch the top tracks.
        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            many="track",
            params=dict(
                method="geo.getTopTracks",
                country=country,
                limit=limit,
                page=page,
            ),
        )

    @classmethod
    def get_top_tracks_chart(
        cls, limit: int = 50, page: int = 1
    ) -> ListModel["Track"]:
        """
        Get the top tracks chart.

        :param limit: The number of results to fetch per page.
        :param page: The page number to fetch.
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return cls.retrieve(
            bind=Track,
            many="track",
            params=dict(method="chart.getTopTracks", limit=limit, page=page),
        )

    def add_tags(self, tags: List[str]) -> RawResponse:
        """
        Tag an track with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this track. Accepts a maximum of 10 tags.
        :type tags: :class:`list` of :class:`str`
        :rtype: :class:`~pydrag.core.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(
                method="track.addTags", track=self.name, tags=",".join(tags)
            ),
        )

    def remove_tag(self, tag: str) -> RawResponse:
        """
        Remove a user's tag from an track.

        :param tag: A single user tag to remove from this track.
        :rtype: :class:`~pydrag.core.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(method="track.removeTag", track=self.name, tag=tag),
        )

    def get_similar(self, limit: int = 50) -> ListModel["Track"]:
        """
        Get all the tracks similar to this track.

        :param limit: Limit the number of similar tracks returned
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.Track`
        """
        return self.retrieve(
            bind=Track,
            many="track",
            params=dict(
                method="track.getSimilar",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
                limit=limit,
            ),
        )

    def get_tags(self, user: str) -> ListModel[Tag]:
        """
        Get the tags applied by an individual user to an track on Last.fm.

        :param user: The username for the context of the request.
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="track.getTags",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> ListModel[Tag]:
        """
        Get the top tags for an track on Last.fm, ordered by popularity.

        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.tag.Tag`
        """
        return self.retrieve(
            bind=Tag,
            many="tag",
            params=dict(
                method="track.getTopTags",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
            ),
        )

    def love(self) -> RawResponse:
        """
        Love a track for a user profile.

        :rtype: :class:`~pydrag.core.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(
                method="track.love", artist=self.artist.name, track=self.name
            ),
        )

    def unlove(self) -> RawResponse:
        """
        Unlove a track for a user profile.

        :rtype: :class:`~pydrag.core.RawResponse`
        """
        return self.submit(
            bind=RawResponse,
            stateful=True,
            params=dict(
                method="track.unlove", artist=self.artist.name, track=self.name
            ),
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
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.ScrobbleTrack`
        """

        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        return ListModel(
            [
                track
                for batch in list(divide_chunks(tracks, min(batch_size, 50)))
                for track in Track._scrobble(batch)
            ]
        )

    @classmethod
    def _scrobble(
        cls, tracks: List[ScrobbleTrack]
    ) -> ListModel[ScrobbleTrack]:
        """
        :param tracks: A list fo tracks to scrobble
        :type tracks: :class:`list` of :class:`~pydrag.models.track.ScrobbleTrack`
        :rtype: :class:`pydrag.core.ListModel` of :class:`~pydrag.models.track.ScrobbleTrack`
        """
        params = dict(method="track.scrobble")
        for idx, track in enumerate(tracks):
            for field, value in track.to_dict().items():
                if value is None:
                    continue
                params.update({"{}[{}]".format(field, idx): value})
        return cls.submit(
            bind=ScrobbleTrack, many="scrobble", stateful=True, params=params
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
        :rtype: :class:`~pydrag.core.RawResponse`
        """

        return cls.submit(
            bind=ScrobbleTrack,
            stateful=True,
            params=dict(
                method="track.updateNowPlaying",
                artist=artist,
                track=track,
                album=album,
                trackNumber=track_number,
                context=context,
                duration=duration,
                albumArtist=album_artist,
            ),
        )
