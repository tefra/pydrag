import os
from unittest import TestCase, mock

from pydrag.models.common import Config, RawResponse, ScrobbleTrack
from pydrag.utils import md5


class RawResponseTests(TestCase):
    def test_to_dict(self):
        raw = RawResponse.from_dict(dict(a=1))
        self.assertEqual(dict(a=1), raw.to_dict())

    def test_from_dict(self):
        raw = RawResponse.from_dict(dict(a=1))
        self.assertEqual(dict(a=1), raw.data)


class ScrobbleTrackTests(TestCase):
    @mock.patch("pydrag.models.common.time.time")
    def test_to_api_dict(self, time):
        time.side_effect = [11111111, 22222222]

        scrobbe = ScrobbleTrack(
            artist="Queen",
            track="We Will Rock You",
            track_number=1,
            album="News of the World",
            album_artist="Queen",
            duration=12,
            mbid="aaaa-bbbb-ccc",
            context="chrome",
            stream_id="something",
            chosen_by_user=True,
        )

        expected = {
            "album": "News of the World",
            "albumArtist": "Queen",
            "artist": "Queen",
            "chosenByUser": True,
            "context": "chrome",
            "duration": 12,
            "mbid": "aaaa-bbbb-ccc",
            "streamId": "something",
            "timestamp": 11111111,
            "track": "We Will Rock You",
            "trackNumber": 1,
        }
        self.assertDictEqual(expected, scrobbe.to_api_dict())

        scrobbe = ScrobbleTrack(artist="Queen", track="We Will Rock You")
        expected = {
            "artist": "Queen",
            "timestamp": 22222222,
            "track": "We Will Rock You",
        }
        self.assertDictEqual(expected, scrobbe.to_api_dict())

        scrobbe = ScrobbleTrack(
            artist="Queen", track="We Will Rock You", timestamp=121212121
        )
        self.assertEqual(121212121, scrobbe.timestamp)


class ConfigTests(TestCase):
    keys = ["api_key", "api_secret", "username", "password", "session"]

    def setUp(self):
        super(ConfigTests, self).setUp()
        self.config = Config.instance()
        Config._instance = None
        for k in self.keys:
            try:
                del os.environ["LASTFM_{}".format(k.upper())]
            except KeyError:
                pass

    def tearDown(self):
        Config._instance = self.config
        super(ConfigTests, self).tearDown()

    def test_instance_from_arguments(self):
        config = Config.instance("key")
        expected = {
            "api_key": "key",
            "api_secret": None,
            "password": None,
            "session": None,
            "username": None,
        }
        self.assertDictEqual(expected, config.to_dict())
        self.assertEqual(config, Config.instance())

        new_config = Config.instance("a", "b", "c", "d", "e")
        expected = {
            "api_key": "a",
            "api_secret": "b",
            "username": "c",
            "password": md5("d"),
            "session": "e",
        }
        self.assertDictEqual(expected, new_config.to_dict())
        self.assertEqual(new_config, Config._instance)
        self.assertNotEqual(config, Config._instance)

    def test_instance_from_environment(self):
        os.environ.update(dict(LASTFM_API_KEY="a"))

        config = Config.instance()
        expected = {
            "api_key": "a",
            "api_secret": None,
            "username": None,
            "password": None,
            "session": None,
        }
        self.assertDictEqual(expected, config.to_dict())

        os.environ.update(
            dict(
                LASTFM_API_KEY="a",
                LASTFM_API_SECRET="b",
                LASTFM_USERNAME="c",
                LASTFM_PASSWORD="d",
                LASTFM_SESSION="e",
            )
        )

        new_config = Config.instance()
        self.assertEqual(config, new_config)
        Config._instance = None
        expected = {
            "api_key": "a",
            "api_secret": "b",
            "username": "c",
            "password": md5("d"),
            "session": "e",
        }

        self.assertDictEqual(expected, Config.instance().to_dict())

    def test_instance_raises_exception(self):
        with self.assertRaises(ValueError) as cm:
            Config.instance()

        self.assertEqual("Provide a valid last.fm api key.", str(cm.exception))
