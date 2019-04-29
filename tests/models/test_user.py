from datetime import datetime

from pydrag.constants import Period
from pydrag.models.common import ListModel
from pydrag.models.user import User
from tests import MethodTestCase, fixture


class UserTests(MethodTestCase):
    def setUp(self):
        self.user = User(
            playlists=None,
            playcount=None,
            gender=None,
            name="rj",
            url=None,
            country=None,
            image=None,
            age=None,
            registered=1037793040,
        )
        self.maxDiff = None
        super(UserTests, self).setUp()

    def test_registered_date(self):
        expected = datetime(2002, 11, 20, 11, 50, 40)
        self.assertEqual(expected, self.user.date_registered)

    @fixture.use_cassette(path="user/get_artist_tracks")
    def test_get_artist_tracks(self):
        result = self.user.get_artist_tracks("Trivium")
        expected_params = {
            "artist": "Trivium",
            "endTimestamp": None,
            "method": "user.getArtistTracks",
            "page": 1,
            "startTimestamp": None,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_artist_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_friends_with_recent_tracks")
    def test_get_friends(self):
        result = self.user.get_friends(recent_tracks=True)
        expected_params = {
            "limit": 50,
            "method": "user.getFriends",
            "page": 1,
            "recenttracks": True,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_friends_with_recent_tracks", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_info")
    def test_get_info(self):
        result = User.find("rj")
        expected_params = {"method": "user.getInfo", "user": "rj"}
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, User)
        self.assertFixtureEqual("user/get_info", result.to_dict())

    @fixture.use_cassette(path="user/get_loved_tracks")
    def test_get_loved_tracks(self):
        result = self.user.get_loved_tracks()
        expected_params = {
            "limit": 50,
            "method": "user.getLovedTracks",
            "page": 1,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_loved_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_personal_tags_track")
    def test_get_personal_tags_track(self):
        result = self.user.get_personal_tags(tag="rock", category="track")
        expected_params = {
            "limit": 50,
            "method": "user.getPersonalTags",
            "page": 1,
            "tag": "rock",
            "taggingtype": "track",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_personal_tags_track", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_personal_tags_album")
    def test_get_personal_tags_album(self):
        self.user.name = "Zaratoustre"
        result = self.user.get_personal_tags(tag="hell", category="album")
        expected_params = {
            "limit": 50,
            "method": "user.getPersonalTags",
            "page": 1,
            "tag": "hell",
            "taggingtype": "album",
            "user": "Zaratoustre",
        }
        self.assertEqual(expected_params, result.params)
        #
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_personal_tags_album", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_personal_tags_artist")
    def test_get_personal_tags_artist(self):
        result = self.user.get_personal_tags(tag="rock", category="artist")
        expected_params = {
            "limit": 50,
            "method": "user.getPersonalTags",
            "page": 1,
            "tag": "rock",
            "taggingtype": "artist",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_personal_tags_artist", result.to_dict()
        )

    def test_get_personal_tags_invalid(self):
        with self.assertRaises(ValueError) as cm:
            self.user.get_personal_tags(tag="rock", category="foo")
        self.assertEqual(
            "Provide a tag type: artist, album or track!", str(cm.exception)
        )

    @fixture.use_cassette(path="user/get_recent_tracks")
    def test_get_recent_tracks(self):
        self.user.name = "Zaratoustre"
        result = self.user.get_recent_tracks()
        expected_params = {
            "extended": True,
            "from": None,
            "limit": 50,
            "method": "user.getRecentTracks",
            "page": 1,
            "to": None,
            "user": "Zaratoustre",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_recent_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_top_albums")
    def test_get_top_albums(self):
        result = self.user.get_top_albums(period=Period.week)
        expected_params = {
            "limit": 50,
            "method": "user.getTopAlbums",
            "page": 1,
            "period": "7day",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_top_albums", result.to_dict())

    @fixture.use_cassette(path="user/get_top_artists")
    def test_get_top_artists(self):
        result = self.user.get_top_artists(period=Period.week)
        expected_params = {
            "limit": 50,
            "method": "user.getTopArtists",
            "page": 1,
            "period": "7day",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_top_artists", result.to_dict())

    @fixture.use_cassette(path="user/get_top_tags")
    def test_get_top_tags(self):
        result = self.user.get_top_tags()
        expected_params = {
            "limit": 50,
            "method": "user.getTopTags",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="user/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.user.get_top_tracks(period=Period.week, limit=1)
        expected_params = {
            "limit": 1,
            "method": "user.getTopTracks",
            "page": 1,
            "period": "7day",
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_weekly_album_chart")
    def test_get_weekly_album_chart(self):
        result = self.user.get_weekly_album_chart()
        expected_params = {
            "from": None,
            "method": "user.getWeeklyAlbumChart",
            "to": None,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_weekly_album_chart", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_weekly_artist_chart")
    def test_get_weekly_artist_chart(self):
        result = self.user.get_weekly_artist_chart()
        expected_params = {
            "from": None,
            "method": "user.getWeeklyArtistChart",
            "to": None,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_weekly_artist_chart", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_weekly_chart_list")
    def test_get_weekly_chart_list(self):
        result = self.user.get_weekly_chart_list()
        expected_params = {"method": "user.getWeeklyChartList", "user": "rj"}
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("user/get_weekly_chart_list", result.to_dict())

    @fixture.use_cassette(path="user/get_weekly_track_chart")
    def test_get_weekly_track_chart(self):
        result = self.user.get_weekly_track_chart()
        expected_params = {
            "from": None,
            "method": "user.getWeeklyTrackChart",
            "to": None,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual(
            "user/get_weekly_track_chart", result.to_dict()
        )

    @fixture.use_cassette(path="library/get_artists")
    def test_get_artists(self):
        result = self.user.get_artists()
        expected_params = {
            "limit": 50,
            "method": "library.getArtists",
            "page": 1,
            "user": "rj",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("library/get_artists", result.to_dict())
