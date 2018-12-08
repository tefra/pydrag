import time
from datetime import datetime, timedelta
from unittest import mock

from pydrag.exceptions import ApiError
from pydrag.models.artist import Artist
from pydrag.models.common import BaseModel, ListModel, RawResponse
from pydrag.models.tests import MethodTestCase, fixture
from pydrag.models.track import ScrobbleTrack, Track


class TrackTests(MethodTestCase):
    def setUp(self):
        self.track = Track(
            artist=Artist(name="AC / DC"), name="Hells Bell", url=None
        )
        super(TrackTests, self).setUp()

    @fixture.use_cassette(path="track/add_tags")
    def test_add_tags(self):
        result = self.track.add_tags(["foo", "bar"])
        expected_params = {
            "method": "track.addTags",
            "tags": "foo,bar",
            "track": "Hells Bell",
        }
        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, RawResponse)
        self.assertIsNone(result.data)

    @fixture.use_cassette(path="track/remove_tag")
    def test_remove_tag(self):
        result = self.track.remove_tag("bar")
        expected_params = {
            "method": "track.removeTag",
            "tag": "bar",
            "track": "Hells Bell",
        }
        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, RawResponse)
        self.assertIsNone(result.data)

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

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("track/get_tags", result.to_dict())

    @fixture.use_cassette(path="track/find")
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
        self.assertFixtureEqual("track/find", result.to_dict())

    @fixture.use_cassette(path="track/find_by_mbid")
    def test_find_by_mbid(self):
        result = Track.find_by_mbid(
            mbid="b6411d6b-2dca-4004-8919-e8c27ff6b286", user="Zaratoustre"
        )
        expected_params = {
            "autocorrect": True,
            "lang": "en",
            "method": "track.getInfo",
            "mbid": "b6411d6b-2dca-4004-8919-e8c27ff6b286",
            "username": "Zaratoustre",
        }

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, Track)
        self.assertFixtureEqual("track/find_by_mbid", result.to_dict())

    @mock.patch.object(Track, "find")
    @mock.patch.object(Track, "find_by_mbid", return_value="Me")
    def test_get_info_when_mbid_is_available(self, find_by_mbid, find):
        self.track.mbid = "b6411d6b-2dca-4004-8919-e8c27ff6b286"
        self.assertEqual("Me", self.track.get_info("rj", "it"))

        self.assertIsNotNone(self.track.mbid)
        find_by_mbid.assert_called_once_with(self.track.mbid, "rj", "it")
        find.assert_not_called()

    @mock.patch.object(Track, "find", return_value="Me")
    @mock.patch.object(Track, "find_by_mbid")
    def test_get_info_when_mbid_is_not_available(self, find_by_mbid, find):
        self.track.mbid = None
        self.assertEqual("Me", self.track.get_info("rj", "it"))

        find.assert_called_once_with(
            self.track.artist.name, self.track.name, "rj", "it"
        )
        find_by_mbid.assert_not_called()

    @fixture.use_cassette(path="track/get_correction")
    def test_get_correction(self):
        result = Track.get_correction(track="Hells Bell", artist="AC / DC")
        expected_params = {
            "artist": "AC / DC",
            "method": "track.getCorrection",
            "track": "Hells Bell",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, Track)
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

        self.assertIsInstance(result, ListModel)
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

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("track/search", result.to_dict())

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

        self.assertIsInstance(result, ListModel)
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
        self.assertIsInstance(result, ScrobbleTrack)
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
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("track/scrobble_tracks", result.to_dict())

    @fixture.use_cassette(path="geo/get_top_tracks")
    def test_get_top_tracks_by_country(self):
        result = Track.get_top_tracks_by_country(
            country="greece", page=1, limit=10
        )
        expected_params = {
            "country": "greece",
            "limit": 10,
            "method": "geo.getTopTracks",
            "page": 1,
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("geo/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="chart/get_top_tracks")
    def test_get_top_tracks_chart(self):
        result = Track.get_top_tracks_chart(limit=10, page=2)
        expected_params = {
            "limit": 10,
            "method": "chart.getTopTracks",
            "page": 2,
        }

        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("chart/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="error_response")
    def test_error_response(self):
        with self.assertRaises(ApiError) as con:
            Track.find(track="Axe and the wind", artist="scorpions")

        self.assertEqual("Track not found", con.exception.message)
        self.assertEqual([], con.exception.links)
        self.assertEqual(6, con.exception.error)