from unittest import TestCase, skip

from lastfm.methods.test import fixture
from lastfm.methods.user import User
from lastfm.models.user import (
    UserArtisttracks,
    User as UserInfo,
    UserFriends,
    UserLovedtracks,
    UserRecenttracks,
    UserTopalbums,
    UserTopartists,
    UserToptracks,
    UserWeeklyalbumchart,
    UserWeeklyartistchart,
    UserWeeklytrackchart,
    UserWeeklychartlist,
    UserToptags,
)


def s(value):
    if type(value) == int:
        return str(value)

    if isinstance(value, list):
        for idx, v in enumerate(value):
            value[idx] = s(v)

    elif isinstance(value, dict):
        if "streamable" in value:
            del value["streamable"]

        for k, v in value.items():
            value[k] = s(v)
    return value


class UserTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.user = User("Zaratoustre")
        super(UserTests, self).setUp()

    def assertDictEqual(self, d1, d2, msg=None):
        super(UserTests, self).assertDictEqual(s(d1), s(d2))

    @fixture.use_cassette(path="user/get_artist_tracks")
    def test_get_artist_tracks(self):
        result = self.user.get_artist_tracks("Trivium")
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserArtisttracks)
        self.assertDictEqual(response["artisttracks"], actual)

    @fixture.use_cassette(path="user/get_friends_with_recent_tracks")
    def test_get_friends(self):
        result = self.user.get_friends(recent_tracks=True)
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["for"] = actual["@attr"]["user"]
        del actual["@attr"]["user"]

        self.assertIsInstance(result, UserFriends)
        self.assertDictEqual(response["friends"], actual)

    @fixture.use_cassette(path="user/get_info")
    def test_get_info(self):
        result = self.user.get_info()
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserInfo)
        self.assertDictEqual(response["user"], actual)

    @fixture.use_cassette(path="user/get_loved_tracks")
    def test_get_loved_tracks(self):
        result = self.user.get_loved_tracks()
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserLovedtracks)
        self.assertDictEqual(response["lovedtracks"], actual)

    @skip("generate data")
    @fixture.use_cassette(path="user/get_personal_tags")
    def test_get_personal_tags(self):
        result = self.user.get_personal_tags(tag="rock", tagging_type="track")
        actual = result.to_dict()
        response = result.response.json()
        self.assertIsInstance(result, UserLovedtracks)
        self.assertDictEqual(response["lovedtracks"], actual)

    @fixture.use_cassette(path="user/get_recent_tracks")
    def test_get_recent_tracks(self):
        result = self.user.get_recent_tracks(extended=False)
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserRecenttracks)
        self.assertDictEqual(response["recenttracks"], actual)

    @fixture.use_cassette(path="user/get_top_albums")
    def test_get_top_albums(self):
        result = self.user.get_top_albums(period="7day")
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserTopalbums)
        self.assertDictEqual(response["topalbums"], actual)

    @fixture.use_cassette(path="user/get_top_artists")
    def test_get_top_artists(self):
        result = self.user.get_top_artists("7day")
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserTopartists)
        self.assertDictEqual(response["topartists"], actual)

    @skip("not enough data")
    @fixture.use_cassette(path="user/get_top_tags")
    def test_get_top_tags(self):
        result = self.user.get_top_tags()
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserToptags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="user/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.user.get_top_tracks(period="7day", limit=1)
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, UserToptracks)
        self.assertDictEqual(response["toptracks"], actual)

    @fixture.use_cassette(path="user/get_weekly_album_chart")
    def test_get_weekly_album_chart(self):
        result = self.user.get_weekly_album_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertIsInstance(result, UserWeeklyalbumchart)
        self.assertDictEqual(response["weeklyalbumchart"], actual)

    @fixture.use_cassette(path="user/get_weekly_artist_chart")
    def test_get_weekly_artist_chart(self):
        result = self.user.get_weekly_artist_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertIsInstance(result, UserWeeklyartistchart)
        self.assertDictEqual(response["weeklyartistchart"], actual)

    @fixture.use_cassette(path="user/get_weekly_chart_list")
    def test_get_weekly_chart_list(self):
        result = self.user.get_weekly_chart_list()
        actual = result.to_dict()["chart"][0]
        response = result.response.json()["weeklychartlist"]["chart"][0]

        actual["from"] = actual["from_date"]
        del actual["from_date"]

        self.assertIsInstance(result, UserWeeklychartlist)
        self.assertDictEqual(response, actual)

    @fixture.use_cassette(path="user/get_weekly_track_chart")
    def test_get_weekly_track_chart(self):
        result = self.user.get_weekly_track_chart()
        actual = result.to_dict()
        response = result.response.json()

        actual["@attr"]["from"] = actual["@attr"]["from_date"]
        del actual["@attr"]["from_date"]

        self.assertIsInstance(result, UserWeeklytrackchart)
        self.assertDictEqual(response["weeklytrackchart"], actual)
