from unittest import mock

from pydrag.models.album import Album
from pydrag.models.common import ListModel
from pydrag.models.common import RawResponse
from tests import fixture
from tests import MethodTestCase


class AlbumTests(MethodTestCase):
    def setUp(self):
        self.album = Album.from_dict(
            {
                "name": "A Night at the Opera",
                "artist": "Queen",
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            }
        )
        super().setUp()

    @fixture.use_cassette(path="album/add_tags")
    def test_add_tags(self):
        result = self.album.add_tags(["foo", "bar"])
        expected_params = {
            "album": "A Night at the Opera",
            "arist": "Queen",
            "method": "album.addTags",
            "tags": "foo,bar",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, RawResponse)
        self.assertIsNone(result.data)

    def test_add_tags_with_no_artist(self):
        self.album.artist = None
        with self.assertRaises(ValueError) as cm:
            self.album.add_tags(["foo", "bar"])

        self.assertEqual("Missing artist name!", str(cm.exception))

    @fixture.use_cassette(path="album/remove_tag")
    def test_remove_tag(self):
        result = self.album.remove_tag("bar")
        expected_params = {
            "album": "A Night at the Opera",
            "artist": "Queen",
            "method": "album.removeTag",
            "tag": "bar",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, RawResponse)
        self.assertIsNone(result.data)

    def test_remove_tags_with_no_artist(self):
        self.album.artist = None
        with self.assertRaises(ValueError) as cm:
            self.album.remove_tag("bar")

        self.assertEqual("Missing artist name!", str(cm.exception))

    @fixture.use_cassette(path="album/get_tags")
    def test_get_tags(self):
        result = self.album.get_tags(user="Zaratoustre")
        expected_params = {
            "album": "A Night at the Opera",
            "artist": "Queen",
            "autocorrect": True,
            "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            "method": "album.getTags",
            "user": "Zaratoustre",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("album/get_tags", result.to_dict())

    def test_get_tags_with_no_artist(self):
        self.album.artist = None
        with self.assertRaises(ValueError) as cm:
            self.album.get_tags("bar")

        self.assertEqual("Missing artist name!", str(cm.exception))

    @fixture.use_cassette(path="album/find")
    def test_find(self):
        result = Album.find(artist="Mumford & Sons", album="Delta")
        expected_params = {
            "album": "Delta",
            "artist": "Mumford & Sons",
            "autocorrect": True,
            "lang": "en",
            "method": "album.getInfo",
            "username": None,
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, Album)
        self.assertFixtureEqual("album/find", result.to_dict())

    @fixture.use_cassette(path="album/find_by_mbid")
    def test_find_by_mbid(self):
        result = Album.find_by_mbid("6defd963-fe91-4550-b18e-82c685603c2b")
        expected_params = {
            "autocorrect": True,
            "lang": "en",
            "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            "method": "album.getInfo",
            "username": None,
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, Album)
        self.assertFixtureEqual("album/find_by_mbid", result.to_dict())

    @mock.patch.object(Album, "find")
    @mock.patch.object(Album, "find_by_mbid", return_value="Me")
    def test_get_info_when_mbid_is_available(self, find_by_mbid, find):
        self.assertEqual("Me", self.album.get_info("rj", "it"))

        self.assertIsNotNone(self.album.mbid)
        find_by_mbid.assert_called_once_with(self.album.mbid, "rj", "it")
        find.assert_not_called()

    @mock.patch.object(Album, "find", return_value="Me")
    @mock.patch.object(Album, "find_by_mbid")
    def test_get_info_when_artist_is_available(self, find_by_mbid, find):
        self.album.mbid = None
        self.assertEqual("Me", self.album.get_info("rj", "it"))

        find.assert_called_once_with(
            self.album.artist.name, self.album.name, "rj", "it"
        )
        find_by_mbid.assert_not_called()

    def test_get_info_with_no_identifier(self):
        self.album.mbid = None
        self.album.artist = None
        with self.assertRaises(ValueError) as cm:
            self.album.get_info("rj", "it")

        self.assertEqual("Missing artist name!", str(cm.exception))

    @fixture.use_cassette(path="album/get_top_tags")
    def test_get_top_tags(self):
        result = self.album.get_top_tags()
        expected_params = {
            "album": "A Night at the Opera",
            "artist": "Queen",
            "autocorrect": True,
            "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            "method": "album.getTopTags",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("album/get_top_tags", result.to_dict())

    def test_get_top_tags_with_no_artist(self):
        self.album.artist = None
        with self.assertRaises(ValueError) as cm:
            self.album.get_top_tags()

        self.assertEqual("Missing artist name!", str(cm.exception))

    @fixture.use_cassette(path="album/search")
    def test_search(self):
        result = Album.search("fire")
        expected_params = {
            "album": "fire",
            "limit": 50,
            "method": "album.search",
            "page": 1,
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ListModel)
        self.assertFixtureEqual("album/search", result.to_dict())
