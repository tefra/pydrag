from typing import List

from pydrag.core import BaseModel
from pydrag.lastfm import POST, api
from pydrag.lastfm.models.track import (
    ScrobbleTrack,
    TrackCorrection,
    TrackInfo,
    TrackScrobble,
    TrackSearch,
    TrackSimilar,
    TrackTags,
    TrackTopTags,
    TrackUpdateNowPlaying,
)


class TrackService:
    """Last.fm Track API interface for easy access/navigation."""

    def __init__(
        self, track: str = None, artist: str = None, mbid: str = None
    ):
        """
        :param track: The track name
        :param mbid: The musicbrainz id for the track
        """
        self.mbid = mbid
        self.track = track
        self.artist = artist

    @api.operation(method=POST, stateful=True)
    def add_tags(self, tags: List[str]) -> BaseModel:
        """
        Tag an track with one or more user supplied tags.

        :param tags: A list of user supplied tags to apply to this track.
        Accepts a maximum of 10 tags.
        :returns: BaseModel
        """
        assert self.track is not None
        return dict(track=self.track, tags=",".join(tags))

    @api.operation(method=POST, stateful=True)
    def remove_tag(self, tag: str) -> BaseModel:
        """
        Remove a user's tag from an track.

        :param tag: A single user tag to remove from this track.
        :returns: BaseModel
        """
        assert self.track is not None
        return dict(track=self.track, tag=tag)

    @api.operation
    def get_info(
        self, autocorrect: bool = True, user: str = None, lang: str = "en"
    ) -> TrackInfo:
        """
        Get the metadata for a track on Last.fm.

        :param autocorrect: If enabled auto correct misspelled names
        :param user: The username for the context of the request.
         If supplied, response will include the user's playcount for this track
        :param lang: The language to return the biography in, ISO 639
        :returns: TrackInfo
        """

        self.assert_mbid_or_track_and_artist()
        return dict(
            mbid=self.mbid,
            track=self.track,
            artist=self.artist,
            autocorrect=autocorrect,
            username=user,
            lang=lang,
        )

    @api.operation
    def get_correction(self) -> TrackCorrection:
        """
        Use the last.fm corrections data to check whether the supplied track
        has a correction to a canonical track.

        :returns: TrackCorrection
        """
        self.assert_mbid_or_track_and_artist()
        return dict(track=self.track, artist=self.artist, mbid=self.mbid)

    @api.operation
    def get_similar(
        self, autocorrect: bool = True, limit: int = 50
    ) -> TrackSimilar:
        """
        Get all the tracks similar to this track.

        :param autocorrect: If enabled auto correct misspelled names
        :param limit: Limit the number of similar tracks returned
        :returns: TrackSimilar
        """
        self.assert_mbid_or_track_and_artist()
        return dict(
            mbid=self.mbid,
            track=self.track,
            artist=self.artist,
            autocorrect=autocorrect,
            limit=limit,
        )

    @api.operation
    def get_tags(self, user: str, autocorrect: bool = True) -> TrackTags:
        """
        Get the tags applied by an individual user to an track on Last.fm.

        :param user: The username for the context of the request.
        :param autocorrect: If enabled auto correct misspelled names
        :returns: TrackTags
        """
        self.assert_mbid_or_track_and_artist()
        return dict(
            mbid=self.mbid,
            track=self.track,
            artist=self.artist,
            autocorrect=autocorrect,
            user=user,
        )

    @api.operation
    def get_top_tags(self, autocorrect: bool = True) -> TrackTopTags:
        """
        Get the top tags for an track on Last.fm, ordered by popularity.

        :param autocorrect: If enabled auto correct misspelled names
        :returns: TrackTopTags
        """
        self.assert_mbid_or_track_and_artist()
        return dict(
            mbid=self.mbid,
            track=self.track,
            artist=self.artist,
            autocorrect=autocorrect,
        )

    @api.operation
    def search(self, limit: int = 50, page: int = 1) -> TrackSearch:
        """
        Search for an track by name. Returns track matches sorted by relevance.

        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :returns: TrackSearch
        """
        assert self.track is not None
        return dict(limit=limit, page=page, track=self.track)

    @api.operation(method=POST, stateful=True)
    def love(self) -> BaseModel:
        """
        Love a track for a user profile.

        :returns: BaseModel
        """
        assert self.track and self.artist
        return dict(artist=self.artist, track=self.track)

    @api.operation(method=POST, stateful=True)
    def unlove(self) -> BaseModel:
        """
        Unlove a track for a user profile.

        :returns: BaseModel
        """
        assert self.track and self.artist
        return dict(artist=self.artist, track=self.track)

    @api.operation(method=POST, stateful=True)
    def scrobble(self, tracks: List[ScrobbleTrack]) -> TrackScrobble:
        params = dict()
        for idx, track in enumerate(tracks):
            for field in track.get_fields():
                value = getattr(track, field.name)
                if value is None:
                    continue
                k = "{}[{}]".format(field.name, idx)
                params.update({k: value})
        return params

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
            result = TrackService().scrobble(batch)
            if status is None:
                status = result
                status.response = None
            elif result.scrobble:
                status.attr.accepted += result.attr.accepted
                status.attr.ignored += result.attr.ignored
                status.scrobble.extend(status.scrobble)
        return status

    @api.operation(method=POST, stateful=True)
    def update_now_playing(
        self,
        album: str = None,
        track_number: int = None,
        context: str = None,
        duration: int = None,
        album_artist: str = None,
    ) -> TrackUpdateNowPlaying:
        """
        :param album: The album name
        :param track_number: The track number of the track on the album
        :param context: Sub-client version (not public)
        :param duration: The length of the track in seconds
        :param album_artist: The album artist
        :return: BaseModel
        """
        assert self.track and self.artist

        return dict(
            artist=self.artist,
            track=self.track,
            album=album,
            trackNumber=track_number,
            context=context,
            duration=duration,
            albumArtist=album_artist,
        )

    def assert_mbid_or_track_and_artist(self):
        assert self.mbid is not None or (
            self.track is not None and self.artist is not None
        )
