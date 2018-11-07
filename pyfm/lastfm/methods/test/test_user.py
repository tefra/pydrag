from unittest import skip

from lastfm.models import (
    UserTopAlbums,
    UserTopArtists,
    UserTopTags,
    UserTopTracks,
    UserWeeklyAlbumChart,
    UserWeeklyArtistChart,
    UserWeeklyChartList,
    UserWeeklyTrackChart,
    UserPersonalTags,
    UserRecentTracks,
    UserFriends,
    UserInfo,
    UserLovedTracks,
    UserArtistTracks,
)
from pyfm.lastfm.methods.test import fixture, MethodTestCase
from pyfm.lastfm.methods.user import User


class UserTests(MethodTestCase):
    def setUp(self):
        self.user = User("rj")
        super(UserTests, self).setUp()

    @fixture.use_cassette(path="user/get_artist_tracks")
    def test_get_artist_tracks(self):
        result = self.user.get_artist_tracks("Trivium")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_artist_tracks", result.method)
        self.assertEqual(
            {"artist": "Trivium", "user": "rj", "page": "1"}, result.params
        )
        self.assertIsNone(None, result.data)
        self.assertIsInstance(result, UserArtistTracks)
        self.assertDictEqual(response["artisttracks"], actual)

    @fixture.use_cassette(path="user/get_friends_with_recent_tracks")
    def test_get_friends(self):
        result = self.user.get_friends(recent_tracks=True)
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["for"] = actual["@attr"]["user"]
        del actual["@attr"]["user"]

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_friends", result.method)
        self.assertEqual(
            {"recenttracks": "1", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertIsInstance(result, UserFriends)
        self.assertDictEqual(response["friends"], actual)

    @fixture.use_cassette(path="user/get_info")
    def test_get_info(self):
        result = self.user.get_info()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertIsInstance(result, UserInfo)
        self.assertDictEqual(response["user"], actual)

    @fixture.use_cassette(path="user/get_loved_tracks")
    def test_get_loved_tracks(self):
        result = self.user.get_loved_tracks()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_loved_tracks", result.method)
        self.assertEqual(
            {"user": "rj", "page": "1", "limit": "50"}, result.params
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, UserLovedTracks)
        self.assertDictEqual(response["lovedtracks"], actual)

    @fixture.use_cassette(path="user/get_personal_tags_track")
    def test_get_personal_tags_track(self):
        result = self.user.get_personal_tags(tag="rock", tagging_type="track")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_personal_tags", result.method)
        self.assertEqual(
            {
                "tag": "rock",
                "taggingtype": "track",
                "user": "rj",
                "page": "1",
                "limit": "50",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.tracks.track), 0)
        self.assertIsInstance(result, UserPersonalTags)
        self.assertDictEqual(response["taggings"], actual)

    @skip("No data")
    @fixture.use_cassette(path="user/get_personal_tags_album")
    def test_get_personal_tags_album(self):
        result = self.user.get_personal_tags(tag="hell", tagging_type="album")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_personal_tags", result.method)
        self.assertEqual(
            {
                "tag": "rock",
                "taggingtype": "artist",
                "user": "rj",
                "page": "1",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.albums.album), 0)
        self.assertIsInstance(result, UserPersonalTags)
        self.assertDictEqual(response["taggings"], actual)

    @fixture.use_cassette(path="user/get_personal_tags_artist")
    def test_get_personal_tags_artist(self):
        result = self.user.get_personal_tags(tag="rock", tagging_type="artist")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_personal_tags", result.method)
        self.assertEqual(
            {
                "tag": "rock",
                "taggingtype": "artist",
                "user": "rj",
                "page": "1",
                "limit": "50",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.artists.artist), 0)
        self.assertIsInstance(result, UserPersonalTags)
        self.assertDictEqual(response["taggings"], actual)

    def test_get_personal_tags_invalid(self):
        with self.assertRaises(AssertionError):
            self.user.get_personal_tags(tag="rock", tagging_type="foo")

    @fixture.use_cassette(path="user/get_recent_tracks")
    def test_get_recent_tracks(self):
        result = self.user.get_recent_tracks(extended=False)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_recent_tracks", result.method)
        self.assertEqual(
            {"extended": "0", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, UserRecentTracks)
        self.assertDictEqual(response["recenttracks"], actual)

    @fixture.use_cassette(path="user/get_top_albums")
    def test_get_top_albums(self):
        result = self.user.get_top_albums(period="7day")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_albums", result.method)
        self.assertEqual(
            {"period": "7day", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.album), 0)
        self.assertIsInstance(result, UserTopAlbums)
        self.assertDictEqual(response["topalbums"], actual)

    @fixture.use_cassette(path="user/get_top_artists")
    def test_get_top_artists(self):
        result = self.user.get_top_artists("7day")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_artists", result.method)
        self.assertEqual(
            {"period": "7day", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.artist), 0)
        self.assertIsInstance(result, UserTopArtists)
        self.assertDictEqual(response["topartists"], actual)

    @fixture.use_cassette(path="user/get_top_tags")
    def test_get_top_tags(self):
        result = self.user.get_top_tags()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual({"user": "rj", "limit": "50"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.tag), 0)
        self.assertIsInstance(result, UserTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="user/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.user.get_top_tracks(period="7day", limit=1)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_tracks", result.method)
        self.assertEqual(
            {
                "limit": "1",
                "period": "7day",
                "user": "rj",
                "page": "1",
                "limit": "1",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, UserTopTracks)
        self.assertDictEqual(response["toptracks"], actual)

    @fixture.use_cassette(path="user/get_weekly_album_chart")
    def test_get_weekly_album_chart(self):
        result = self.user.get_weekly_album_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_album_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.album), 0)
        self.assertIsInstance(result, UserWeeklyAlbumChart)
        self.assertDictEqual(response["weeklyalbumchart"], actual)

    @fixture.use_cassette(path="user/get_weekly_artist_chart")
    def test_get_weekly_artist_chart(self):
        result = self.user.get_weekly_artist_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_artist_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.artist), 0)
        self.assertIsInstance(result, UserWeeklyArtistChart)
        self.assertDictEqual(response["weeklyartistchart"], actual)

    @fixture.use_cassette(path="user/get_weekly_chart_list")
    def test_get_weekly_chart_list(self):
        result = self.user.get_weekly_chart_list()
        actual = result.to_dict()["chart"][0]
        response = result.response.json()["weeklychartlist"]["chart"][0]

        actual["from"] = actual["from_date"]
        del actual["from_date"]

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_chart_list", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.chart), 0)
        self.assertIsInstance(result, UserWeeklyChartList)
        self.assertDictEqual(response, actual)

    @fixture.use_cassette(path="user/get_weekly_track_chart")
    def test_get_weekly_track_chart(self):
        result = self.user.get_weekly_track_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_track_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, UserWeeklyTrackChart)
        self.assertDictEqual(response["weeklytrackchart"], actual)
