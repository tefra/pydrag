from typing import List, Optional, TypeVar

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.album import AlbumInfo
from pydrag.lastfm.models.common import (
    Attributes,
    Image,
    OpenSearch,
    SimpleArtist,
    TagList,
    Tags,
    Track,
    TrackList,
    TrackSimpleArtist,
    Wiki,
)


@dataclass
class TrackInfo(Track):
    wiki: Wiki = None
    album: AlbumInfo = None
    top_tags: Tags = None


@dataclass
class CorrectionTrack(BaseModel):
    attr: Attributes
    track: TrackInfo = None


@dataclass
class TrackCorrection(BaseModel):
    correction: CorrectionTrack


@dataclass
class TrackMatches(BaseModel):
    track: List[TrackSimpleArtist]


@dataclass
class TrackSearch(OpenSearch):
    matches: TrackMatches


@dataclass
class Corrected(BaseModel):
    text: str = None
    code: str = None
    corrected: int = None


@dataclass
class TrackUpdateNowPlaying(BaseModel):
    album: Corrected = None
    artist: Corrected = None
    track: Corrected = None
    timestamp: int = None
    ignored_message: Corrected = None
    album_artist: Corrected = None
    attr: Attributes = None


@dataclass
class TrackScrobble(BaseModel):
    scrobble: List[TrackUpdateNowPlaying]
    attr: Attributes

    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data, dict) and data.get("scrobble"):
            if isinstance(data["scrobble"], dict):
                data["scrobble"] = [data["scrobble"]]
        return super().from_dict(data)


@dataclass
class ScrobbleTrack(BaseModel):
    artist: str
    track: str
    timestamp: int
    album: str = None
    context: str = None
    stream_id: str = None
    chosen_by_user: bool = None
    track_number: str = None
    mbid: str = None
    album_artist: str = None
    duration: int = None


T = TypeVar("T", bound="Track")


@dataclass
class Track(BaseModel):
    name: str
    url: str
    artist: SimpleArtist
    mbid: str = None
    image: List[Image] = None
    playcount: int = None
    listeners: int = None
    streamable: str = None
    duration: str = None
    match: Optional[float] = None
    wiki: Wiki = None
    album: AlbumInfo = None
    top_tags: Tags = None
    attr: Attributes = None

    @classmethod
    def from_artist_track(cls, artist: str, track: str):
        return Track(artist=SimpleArtist(name=artist), name=track, url=None)

    @classmethod
    def find(
        cls, artist: str, track: str, user: str = None, lang: str = "en"
    ) -> T:

        """
        Get the metadata for a track on Last.fm.

        :param artist: The artist name
        :param track: The track name
        :param user: The username for the context of the request.
         If supplied, response will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :returns: Track
        """
        return cls.retrieve(
            params=dict(
                method="track.getInfo",
                artist=artist,
                track=track,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def find_by_mbid(cls, mbid: str, user: str = None, lang: str = "en") -> T:
        """
        Get the metadata for a track on Last.fm.

        :param mbid: The musicbrainz id for the track
        :param user: The username for the context of the request.
         If supplied, response will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :returns: Track
        """
        return cls.retrieve(
            params=dict(
                method="track.getInfo",
                mbid=mbid,
                autocorrect=True,
                username=user,
                lang=lang,
            )
        )

    @classmethod
    def get_correction(cls, track: str, artist: str) -> TrackCorrection:
        """
        Use the last.fm corrections data to check whether the supplied track
        has a correction to a canonical track.

        :returns: TrackCorrection
        """
        return cls.retrieve(
            bind=TrackCorrection,
            params=dict(
                method="track.getCorrection", artist=artist, track=track
            ),
        )

    @classmethod
    def search(cls, track: str, limit: int = 50, page: int = 1) -> TrackSearch:
        """
        Search for an track by name. Returns track matches sorted by relevance.

        :param str track: The track name.
        :param int page: The page number to fetch.
        :param int limit: The number of results to fetch per page.
        :returns: TrackSearch
        """
        return cls.retrieve(
            bind=TrackSearch,
            params=dict(
                method="track.search", limit=limit, page=page, track=track
            ),
        )

    @classmethod
    def get_top_tracks_by_country(
        cls, country: str, limit: int = 50, page: int = 1
    ) -> TrackList:
        """
        :param country: The country to fetch the top tracks.
        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TrackList
        """
        return cls.retrieve(
            bind=TrackList,
            params=dict(
                method="geo.getTopTracks",
                country=country,
                limit=limit,
                page=page,
            ),
        )

    @classmethod
    def get_top_tracks_chart(cls, limit: int = 50, page: int = 1) -> TrackList:
        """
        Get the top tracks chart.

        :param int limit: The number of results to fetch per page.
        :param int page: The page number to fetch. Defaults to first page.
        :returns: TrackList
        """
        return cls.retrieve(
            bind=TrackList,
            params=dict(method="chart.getTopTracks", limit=limit, page=page),
        )

    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an track with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this track. Accepts a maximum of 10 tags.
        :returns: BaseModel
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="track.addTags", track=self.name, tags=",".join(tags)
            ),
        )

    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an track.

        :param tag: A single user tag to remove from this track.
        :returns: BaseModel
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(method="track.removeTag", track=self.name, tag=tag),
        )

    def get_similar(self, limit: int = 50) -> TrackList:
        """
        Get all the tracks similar to this track.

        :param int limit: Limit the number of similar tracks returned
        :returns: TrackSimilar
        """
        return self.retrieve(
            bind=TrackList,
            params=dict(
                method="track.getSimilar",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
                limit=limit,
            ),
        )

    def get_tags(self, user: str) -> TagList:
        """
        Get the tags applied by an individual user to an track on Last.fm.

        :param user: The username for the context of the request.
        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="track.getTags",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
                user=user,
            ),
        )

    def get_top_tags(self) -> TagList:
        """
        Get the top tags for an track on Last.fm, ordered by popularity.

        :returns: TagList
        """
        return self.retrieve(
            bind=TagList,
            params=dict(
                method="track.getTopTags",
                mbid=self.mbid,
                artist=self.artist.name,
                track=self.name,
                autocorrect=True,
            ),
        )

    def love(self) -> BaseModel:
        """
        Love a track for a user profile.

        :returns: BaseModel
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="track.love", artist=self.artist.name, track=self.name
            ),
        )

    def unlove(self) -> BaseModel:
        """
        Unlove a track for a user profile.

        :returns: BaseModel
        """
        return self.submit(
            bind=BaseModel,
            stateful=True,
            params=dict(
                method="track.unlove", artist=self.artist.name, track=self.name
            ),
        )

    @classmethod
    def scrobble(cls, tracks: List[ScrobbleTrack]) -> TrackScrobble:
        params = dict(method="track.scrobble")
        for idx, track in enumerate(tracks):
            for field, value in track.to_dict().items():
                if value is None:
                    continue
                params.update({"{}[{}]".format(field, idx): value})
        return cls.submit(bind=TrackScrobble, stateful=True, params=params)

    @classmethod
    def scrobble_tracks(
        cls, tracks: List[ScrobbleTrack], batch_size=10
    ) -> TrackScrobble:
        """
        Split tracks into the desired batch size, with maximum size set to 50
        and send the tracks for processing, I am debating if this even belongs
        here.

        :param tracks: The tracks to scrobble
        :param batch_size: The number of tracks to submit per cycle
        :returns: TrackScrobble: after we aggregate the results
        """
        batch_size = min(batch_size, 50)

        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        status = None
        batches = list(divide_chunks(tracks, batch_size))
        for batch in batches:
            result = Track.scrobble(batch)
            if status is None:
                status = result
                status.response = None
            elif result.scrobble:
                status.attr.accepted += result.attr.accepted
                status.attr.ignored += result.attr.ignored
                status.scrobble.extend(status.scrobble)
        return status

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
    ) -> TrackUpdateNowPlaying:
        """
        :param artist: The artist name
        :param track: The track name
        :param album: The album name
        :param track_number: The track number of the track on the album
        :param context: Sub-client version (not public)
        :param duration: The length of the track in seconds
        :param album_artist: The album artist
        :return: BaseModel
        """

        return cls.submit(
            bind=TrackUpdateNowPlaying,
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
