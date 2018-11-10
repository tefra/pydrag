import time
from datetime import datetime, timedelta
from unittest import skip

from pyfm.lastfm.services import TrackService
from pyfm.lastfm.services.test import fixture, MethodTestCase
from pyfm.lastfm.models import (
    BaseModel,
    TrackTags,
    TrackInfo,
    TrackTopTags,
    TrackSearch,
    TrackCorrection,
    TrackSimilar,
    TrackUpdateNowPlaying,
    ScrobbleTrack,
    TrackScrobble,
)


class TrackServiceTests(MethodTestCase):
    def setUp(self):
        self.track = TrackService(track="Hells Bell", artist="AC / DC")
        super(TrackServiceTests, self).setUp()

    @fixture.use_cassette(path="track/add_tags")
    def test_add_tags(self):
        result = self.track.add_tags(["foo", "bar"])
        self.assertDictEqual(
            {"track": "Hells Bell", "sk": "CENSORED", "tags": "foo,bar"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @skip("wth where is my tag list")
    @fixture.use_cassette(path="track/get_tags")
    def test_get_tags(self):
        result = self.track.get_tags(user="Zaratoustre")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_tags", result.method)
        self.assertDictEqual(
            {
                "artist": "AC / DC",
                "track": "Hells Bell",
                "autocorrect": True,
                "user": "Zaratoustre",
            },
            result.params,
        )
        self.assertIsInstance(result, TrackTags)
        self.assertDictEqual(response["tags"], actual)

    @fixture.use_cassette(path="track/remove_tag")
    def test_remove_tag(self):
        result = self.track.remove_tag("bar")
        self.assertDictEqual(
            {"track": "Hells Bell", "sk": "CENSORED", "tag": "bar"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/get_info")
    def test_get_info(self):
        self.track.mbid = None
        result = self.track.get_info()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertDictEqual(
            {
                "artist": "AC / DC",
                "track": "Hells Bell",
                "autocorrect": True,
                "lang": "en",
            },
            result.params,
        )
        self.assertIsInstance(result, TrackInfo)
        self.assertDictEqual(response["track"], actual)

    @fixture.use_cassette(path="track/get_correction")
    def test_get_correction(self):
        self.track.track = "Hells Bell"
        result = self.track.get_correction()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_correction", result.method)
        self.assertEqual(
            {"artist": "AC / DC", "track": "Hells Bell"}, result.params
        )
        self.assertIsInstance(result, TrackCorrection)
        self.assertDictEqual(response["corrections"], actual)

    @fixture.use_cassette(path="track/get_top_tags")
    def test_get_top_tags(self):
        result = self.track.get_top_tags(True)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual(
            {"artist": "AC / DC", "autocorrect": True, "track": "Hells Bell"},
            result.params,
        )
        self.assertGreater(len(result.tag), 0)
        self.assertIsInstance(result, TrackTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="track/search")
    def test_search(self):
        self.track.track = "gun"
        result = self.track.search()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("search", result.method)
        self.assertEqual(
            {"track": "gun", "page": "1", "limit": "50"}, result.params
        )

        self.assertGreater(len(result.trackmatches.track), 0)
        self.assertIsInstance(result, TrackSearch)
        self.assertDictEqual(response["results"], actual)

    @fixture.use_cassette(path="track/get_similar")
    def test_get_similar(self):
        result = self.track.get_similar(True)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_similar", result.method)
        self.assertEqual(
            {
                "artist": "AC / DC",
                "autocorrect": True,
                "limit": "50",
                "track": "Hells Bell",
            },
            result.params,
        )
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, TrackSimilar)
        self.assertDictEqual(response["similartracks"], actual)

    @fixture.use_cassette(path="track/love")
    def test_love(self):
        result = TrackService(track="Hells Bells", artist="AC / DC").love()
        self.assertDictEqual(
            {"artist": "AC / DC", "sk": "CENSORED", "track": "Hells Bells"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/unlove")
    def test_unlove(self):
        result = TrackService(track="Hells Bells", artist="AC / DC").unlove()
        self.assertDictEqual(
            {"artist": "AC / DC", "sk": "CENSORED", "track": "Hells Bells"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/update_now_playing")
    def test_update_now_playing(self):
        result = TrackService(
            track="Hells Bells", artist="AC/DC"
        ).update_now_playing(track_number=2)
        response = result.response.json()
        actual = result.to_dict()
        self.assertDictEqual(
            {
                "artist": "AC/DC",
                "sk": "CENSORED",
                "track": "Hells Bells",
                "trackNumber": "2",
            },
            result.params,
        )
        self.assertIsInstance(result, TrackUpdateNowPlaying)
        self.assertDictEqual(response["nowplaying"], actual)

    @fixture.use_cassette(path="track/scrobble_tracks")
    def test_scrobble_tracks(self):
        entries = (
            ("Green Day", "Bang Bang"),
            ("Awolnation", "Sail"),
            ("The Head and the Heart", "All We Ever Knew"),
            ("Kaleo", "Way Down We Go"),
            ("Disturbed", "The Sound of Silence"),
        )

        tracks = []
        date = datetime(year=2018, month=11, day=10, hour=21, minute=30)
        for artist, track in entries:
            next = date + timedelta(minutes=5)
            timestamp = int(time.mktime(next.timetuple()))
            tracks.append(
                ScrobbleTrack(artist=artist, track=track, timestamp=timestamp)
            )

        result = TrackService.scrobble_tracks(tracks, batch_size=2)
        actual = result.to_dict()
        expected = {
            "@attr": {"accepted": "5", "ignored": "0"},
            "scrobble": [
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Green Day", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Bang Bang", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Awolnation", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Sail", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Green Day", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Bang Bang", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Awolnation", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Sail", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Green Day", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Bang Bang", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Awolnation", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Sail", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Green Day", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Bang Bang", "corrected": "0"},
                },
                {
                    "album": {"corrected": "0"},
                    "albumArtist": {"#text": "", "corrected": "0"},
                    "artist": {"#text": "Awolnation", "corrected": "0"},
                    "ignoredMessage": {"#text": "", "code": "0"},
                    "timestamp": "1541878500",
                    "track": {"#text": "Sail", "corrected": "0"},
                },
            ],
        }

        self.assertIsInstance(result, TrackScrobble)
        self.assertDictEqual(expected, actual)
