from pydrag.core import BaseModel
from pydrag.lastfm.models.album import Album, AlbumSearch
from pydrag.lastfm.models.common import TagList
from pydrag.lastfm.models.test import MethodTestCase, fixture


class AlbumServiceTests(MethodTestCase):
    def setUp(self):
        self.album = Album(
            name="A Night at the Opera",
            artist="Queen",
            mbid="6defd963-fe91-4550-b18e-82c685603c2b",
        )
        super(AlbumServiceTests, self).setUp()

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

        self.assertIsInstance(result, BaseModel)

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

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("album/get_tags", result.to_dict())

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

        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="album/get_info")
    def test_find(self):
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
        self.assertFixtureEqual("album/get_info", result.to_dict())

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

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("album/get_top_tags", result.to_dict())

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

        self.assertIsInstance(result, AlbumSearch)
        self.assertFixtureEqual("album/search", result.to_dict())

        self.assertEqual(1, result.get_page())
        self.assertEqual(50, result.get_limit())
        self.assertEqual(661041, result.get_total())
        self.assertEqual(13221, result.get_total_pages())
        self.assertFalse(result.has_prev())
        self.assertTrue(result.has_next())
