from pydrag.lastfm import Period
from pydrag.lastfm.models.common import (
    AlbumList,
    ArtistList,
    ChartList,
    TagList,
    TrackList,
)
from pydrag.lastfm.models.user import (
    ArtistTrackList,
    UserFriends,
    UserInfo,
    UserPersonalTags,
)
from pydrag.lastfm.services.test import MethodTestCase, fixture
from pydrag.lastfm.services.user import UserService


class UserServiceTests(MethodTestCase):
    def setUp(self):
        self.user = UserService("rj")
        super(UserServiceTests, self).setUp()

    @fixture.use_cassette(path="user/get_artist_tracks")
    def test_get_artist_tracks(self):
        result = self.user.get_artist_tracks("Trivium")

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_artist_tracks", result.method)
        self.assertEqual(
            {"artist": "Trivium", "user": "rj", "page": "1"}, result.params
        )
        self.assertIsInstance(result, ArtistTrackList)
        self.assertFixtureEqual("user/get_artist_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_friends_with_recent_tracks")
    def test_get_friends(self):
        result = self.user.get_friends(recent_tracks=True)

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_friends", result.method)
        self.assertEqual(
            {"recenttracks": True, "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )
        self.assertIsInstance(result, UserFriends)
        self.assertFixtureEqual(
            "user/get_friends_with_recent_tracks", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_info")
    def test_get_info(self):
        result = self.user.get_info()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertEqual({"user": "rj"}, result.params)
        self.assertIsInstance(result, UserInfo)
        self.assertFixtureEqual("user/get_info", result.to_dict())

    @fixture.use_cassette(path="user/get_loved_tracks")
    def test_get_loved_tracks(self):
        result = self.user.get_loved_tracks()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_loved_tracks", result.method)
        self.assertEqual(
            {"user": "rj", "page": "1", "limit": "50"}, result.params
        )

        self.assertIsInstance(result, ArtistTrackList)
        self.assertFixtureEqual("user/get_loved_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_personal_tags_track")
    def test_get_personal_tags_track(self):
        result = self.user.get_personal_tags(tag="rock", tagging_type="track")

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

        self.assertIsInstance(result, UserPersonalTags)
        self.assertFixtureEqual(
            "user/get_personal_tags_track", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_personal_tags_album")
    def test_get_personal_tags_album(self):
        self.user.user = "Zaratoustre"
        result = self.user.get_personal_tags(tag="hell", tagging_type="album")

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_personal_tags", result.method)
        self.assertEqual(
            {
                "tag": "hell",
                "taggingtype": "album",
                "user": "Zaratoustre",
                "page": 1,
                "limit": 50,
            },
            result.params,
        )
        #
        self.assertIsInstance(result, UserPersonalTags)
        self.assertFixtureEqual(
            "user/get_personal_tags_album", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_personal_tags_artist")
    def test_get_personal_tags_artist(self):
        result = self.user.get_personal_tags(tag="rock", tagging_type="artist")

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

        self.assertIsInstance(result, UserPersonalTags)
        self.assertFixtureEqual(
            "user/get_personal_tags_artist", result.to_dict()
        )

    def test_get_personal_tags_invalid(self):
        with self.assertRaises(AssertionError):
            self.user.get_personal_tags(tag="rock", tagging_type="foo")

    @fixture.use_cassette(path="user/get_recent_tracks")
    def test_get_recent_tracks(self):
        result = self.user.get_recent_tracks(extended=False)

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_recent_tracks", result.method)
        self.assertEqual(
            {"extended": False, "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )

        self.assertIsInstance(result, ArtistTrackList)
        self.assertFixtureEqual("user/get_recent_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_top_albums")
    def test_get_top_albums(self):
        result = self.user.get_top_albums(period=Period.week)

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_albums", result.method)
        self.assertEqual(
            {"period": "7day", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )

        self.assertIsInstance(result, AlbumList)
        self.assertFixtureEqual("user/get_top_albums", result.to_dict())

    @fixture.use_cassette(path="user/get_top_artists")
    def test_get_top_artists(self):
        result = self.user.get_top_artists(period=Period.week)

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_artists", result.method)
        self.assertEqual(
            {"period": "7day", "user": "rj", "page": "1", "limit": "50"},
            result.params,
        )

        self.assertIsInstance(result, ArtistList)
        self.assertFixtureEqual("user/get_top_artists", result.to_dict())

    @fixture.use_cassette(path="user/get_top_tags")
    def test_get_top_tags(self):
        result = self.user.get_top_tags()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual({"user": "rj", "limit": "50"}, result.params)

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("user/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="user/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.user.get_top_tracks(period=Period.week, limit=1)

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_top_tracks", result.method)
        self.assertEqual(
            {"period": "7day", "user": "rj", "page": "1", "limit": "1"},
            result.params,
        )

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual("user/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="user/get_weekly_album_chart")
    def test_get_weekly_album_chart(self):
        result = self.user.get_weekly_album_chart()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_album_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)

        self.assertIsInstance(result, AlbumList)
        self.assertFixtureEqual(
            "user/get_weekly_album_chart", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_weekly_artist_chart")
    def test_get_weekly_artist_chart(self):
        result = self.user.get_weekly_artist_chart()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_artist_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)

        self.assertIsInstance(result, ArtistList)
        self.assertFixtureEqual(
            "user/get_weekly_artist_chart", result.to_dict()
        )

    @fixture.use_cassette(path="user/get_weekly_chart_list")
    def test_get_weekly_chart_list(self):
        result = self.user.get_weekly_chart_list()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_chart_list", result.method)
        self.assertEqual({"user": "rj"}, result.params)

        self.assertIsInstance(result, ChartList)
        self.assertFixtureEqual("user/get_weekly_chart_list", result.to_dict())

    @fixture.use_cassette(path="user/get_weekly_track_chart")
    def test_get_weekly_track_chart(self):
        result = self.user.get_weekly_track_chart()

        self.assertEqual("User", result.namespace)
        self.assertEqual("get_weekly_track_chart", result.method)
        self.assertEqual({"user": "rj"}, result.params)

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual(
            "user/get_weekly_track_chart", result.to_dict()
        )
