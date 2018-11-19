import time
from datetime import datetime, timedelta

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import TagList, TrackList
from pydrag.lastfm.models.track import (
    ScrobbleTrack,
    TrackCorrection,
    TrackInfo,
    TrackScrobble,
    TrackSearch,
    TrackUpdateNowPlaying,
)
from pydrag.lastfm.services.test import MethodTestCase, fixture
from pydrag.lastfm.services.track import TrackService


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

    @fixture.use_cassette(path="track/get_tags")
    def test_get_tags(self):
        result = self.track.get_tags(user="RJ")

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_tags", result.method)
        self.assertDictEqual(
            {
                "artist": "AC / DC",
                "autocorrect": True,
                "track": "Hells Bell",
                "user": "RJ",
            },
            result.params,
        )

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("track/get_tags", result.to_dict())

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
        self.assertFixtureEqual("track/get_info", result.to_dict())

    @fixture.use_cassette(path="track/get_correction")
    def test_get_correction(self):
        self.track.track = "Hells Bell"
        result = self.track.get_correction()

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_correction", result.method)
        self.assertEqual(
            {"artist": "AC / DC", "track": "Hells Bell"}, result.params
        )
        self.assertIsInstance(result, TrackCorrection)
        self.assertFixtureEqual("track/get_correction", result.to_dict())

    @fixture.use_cassette(path="track/get_top_tags")
    def test_get_top_tags(self):
        result = self.track.get_top_tags(True)

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual(
            {"artist": "AC / DC", "autocorrect": True, "track": "Hells Bell"},
            result.params,
        )

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("track/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="track/search")
    def test_search(self):
        self.track.track = "gun"
        result = self.track.search(page=4, limit=5)

        self.assertEqual("Track", result.namespace)
        self.assertEqual("search", result.method)
        self.assertEqual(
            {"track": "gun", "page": 4, "limit": 5}, result.params
        )

        self.assertIsInstance(result, TrackSearch)
        self.assertFixtureEqual("track/search", result.to_dict())

        self.assertEqual(4, result.get_page())
        self.assertEqual(5, result.get_limit())
        self.assertEqual(1443087, result.get_total())
        self.assertEqual(288618, result.get_total_pages())
        self.assertTrue(result.has_prev())
        self.assertTrue(result.has_next())

    @fixture.use_cassette(path="track/get_similar")
    def test_get_similar(self):
        result = self.track.get_similar(True)

        self.assertEqual("Track", result.namespace)
        self.assertEqual("get_similar", result.method)
        self.assertEqual(
            {
                "artist": "AC / DC",
                "autocorrect": True,
                "limit": 50,
                "track": "Hells Bell",
            },
            result.params,
        )

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual("track/get_similar", result.to_dict())

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
        result.response.json()
        result.to_dict()
        self.assertDictEqual(
            {
                "artist": "AC/DC",
                "sk": "CENSORED",
                "track": "Hells Bells",
                "trackNumber": 2,
            },
            result.params,
        )
        self.assertIsInstance(result, TrackUpdateNowPlaying)
        self.assertFixtureEqual("track/update_now_playing", result.to_dict())

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
            _next = date + timedelta(minutes=5)
            timestamp = int(time.mktime(_next.timetuple()))
            tracks.append(
                ScrobbleTrack(artist=artist, track=track, timestamp=timestamp)
            )

        result = TrackService.scrobble_tracks(tracks, batch_size=2)
        actual = result.to_dict()
        expected = {
            "attr": {"accepted": 5, "ignored": 0},
            "scrobble": [
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Green Day", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Bang Bang", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Awolnation", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Sail", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Green Day", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Bang Bang", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Awolnation", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Sail", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Green Day", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Bang Bang", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Awolnation", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Sail", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Green Day", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Bang Bang", "corrected": 0},
                },
                {
                    "album": {"corrected": 0},
                    "album_artist": {"text": "", "corrected": 0},
                    "artist": {"text": "Awolnation", "corrected": 0},
                    "ignored_message": {"text": "", "code": "0"},
                    "timestamp": 1541878500,
                    "track": {"text": "Sail", "corrected": 0},
                },
            ],
        }

        self.assertIsInstance(result, TrackScrobble)
        self.assertDictEqual(expected, actual)
