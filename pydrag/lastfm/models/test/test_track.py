import time
from datetime import datetime, timedelta

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import TagList, TrackList
from pydrag.lastfm.models.test import MethodTestCase, fixture
from pydrag.lastfm.models.track import (
    ScrobbleTrack,
    Track,
    TrackCorrection,
    TrackScrobble,
    TrackSearch,
    TrackUpdateNowPlaying,
)


class TrackServiceTests(MethodTestCase):
    def setUp(self):
        self.track = Track.from_artist_track(
            artist="AC / DC", track="Hells Bell"
        )
        super(TrackServiceTests, self).setUp()

    @fixture.use_cassette(path="track/add_tags")
    def test_add_tags(self):
        result = self.track.add_tags(["foo", "bar"])
        expected_params = {
            "method": "track.addTags",
            "tags": "foo,bar",
            "track": "Hells Bell",
        }
        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/get_tags")
    def test_get_tags(self):
        result = self.track.get_tags(user="RJ")
        expected_params = {
            "artist": "AC / DC",
            "autocorrect": True,
            "mbid": None,
            "method": "track.getTags",
            "track": "Hells Bell",
            "user": "RJ",
        }

        self.assertDictEqual(expected_params, result.params)

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("track/get_tags", result.to_dict())

    @fixture.use_cassette(path="track/remove_tag")
    def test_remove_tag(self):
        result = self.track.remove_tag("bar")
        expected_params = {
            "method": "track.removeTag",
            "tag": "bar",
            "track": "Hells Bell",
        }
        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/get_info")
    def test_find(self):
        result = Track.find(artist="AC / DC", track="Hells Bell")
        expected_params = {
            "artist": "AC / DC",
            "autocorrect": True,
            "lang": "en",
            "method": "track.getInfo",
            "track": "Hells Bell",
            "username": None,
        }

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, Track)
        self.assertFixtureEqual("track/get_info", result.to_dict())

    @fixture.use_cassette(path="track/get_correction")
    def test_get_correction(self):
        result = Track.get_correction(track="Hells Bell", artist="AC / DC")
        expected_params = {
            "artist": "AC / DC",
            "method": "track.getCorrection",
            "track": "Hells Bell",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, TrackCorrection)
        self.assertFixtureEqual("track/get_correction", result.to_dict())

    @fixture.use_cassette(path="track/get_top_tags")
    def test_get_top_tags(self):
        result = self.track.get_top_tags()
        expected_params = {
            "artist": "AC / DC",
            "autocorrect": True,
            "mbid": None,
            "method": "track.getTopTags",
            "track": "Hells Bell",
        }

        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("track/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="track/search")
    def test_search(self):
        result = Track.search(track="gun", page=4, limit=5)

        expected_params = {
            "limit": 5,
            "method": "track.search",
            "page": 4,
            "track": "gun",
        }

        self.assertEqual(expected_params, result.params)

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
        result = self.track.get_similar()
        expected_params = {
            "artist": "AC / DC",
            "autocorrect": True,
            "limit": 50,
            "mbid": None,
            "method": "track.getSimilar",
            "track": "Hells Bell",
        }

        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual("track/get_similar", result.to_dict())

    @fixture.use_cassette(path="track/love")
    def test_love(self):
        result = self.track.love()
        expected_params = {
            "artist": "AC / DC",
            "method": "track.love",
            "track": "Hells Bell",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/unlove")
    def test_unlove(self):
        result = self.track.unlove()
        expected_params = {
            "artist": "AC / DC",
            "method": "track.unlove",
            "track": "Hells Bell",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="track/update_now_playing")
    def test_update_now_playing(self):
        result = Track.update_now_playing(
            track="Hells Bells", artist="AC/DC", track_number=2
        )
        expected_params = {
            "album": None,
            "albumArtist": None,
            "artist": "AC/DC",
            "context": None,
            "duration": None,
            "method": "track.updateNowPlaying",
            "track": "Hells Bells",
            "trackNumber": 2,
        }
        self.assertEqual(expected_params, result.params)
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

        result = Track.scrobble_tracks(tracks, batch_size=2)
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
