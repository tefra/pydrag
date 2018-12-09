from unittest import TestCase, mock

from pydrag.models.common import RawResponse, ScrobbleTrack


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
