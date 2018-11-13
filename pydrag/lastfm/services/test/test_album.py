from pydrag.core import BaseModel
from pydrag.lastfm.models.album import (
    AlbumInfo,
    AlbumSearch,
    AlbumTags,
    AlbumTopTags,
)
from pydrag.lastfm.services.album import AlbumService
from pydrag.lastfm.services.test import MethodTestCase, fixture


class AlbumServiceTests(MethodTestCase):
    def setUp(self):
        self.album = AlbumService(
            album="A Night at the Opera",
            artist="Queen",
            mbid="6defd963-fe91-4550-b18e-82c685603c2b",
        )
        super(AlbumServiceTests, self).setUp()

    @fixture.use_cassette(path="album/add_tags")
    def test_add_tags(self):
        result = self.album.add_tags(["foo", "bar"])
        self.assertDictEqual(
            {
                "album": "A Night at the Opera",
                "artist": "Queen",
                "sk": "CENSORED",
                "tags": "foo,bar",
            },
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="album/get_tags")
    def test_get_tags(self):
        result = self.album.get_tags(user="Zaratoustre")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Album", result.namespace)
        self.assertEqual("get_tags", result.method)
        self.assertEqual(
            {
                "album": "A Night at the Opera",
                "artist": "Queen",
                "autocorrect": True,
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
                "user": "Zaratoustre",
            },
            result.params,
        )
        self.assertIsInstance(result, AlbumTags)
        self.assertEqual(2, len(result.tag))
        self.assertDictEqual(response["tags"], actual)

    @fixture.use_cassette(path="album/remove_tag")
    def test_remove_tag(self):
        result = self.album.remove_tag("bar")
        self.assertDictEqual(
            {
                "album": "A Night at the Opera",
                "artist": "Queen",
                "sk": "CENSORED",
                "tag": "bar",
            },
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="album/get_info")
    def test_get_info(self):
        self.album.artist = None
        self.album.album = None
        result = self.album.get_info()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Album", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertEqual(
            {
                "autocorrect": True,
                "lang": "en",
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            },
            result.params,
        )
        self.assertIsInstance(result, AlbumInfo)
        self.assertDictEqual(response["album"], actual)

    @fixture.use_cassette(path="album/get_top_tags")
    def test_get_top_tags(self):
        result = self.album.get_top_tags(False)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Album", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual(
            {
                "album": "A Night at the Opera",
                "artist": "Queen",
                "autocorrect": False,
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            },
            result.params,
        )
        self.assertGreater(len(result.tag), 0)
        self.assertIsInstance(result, AlbumTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="album/search")
    def test_search(self):
        self.album.album = "fire"
        result = self.album.search()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Album", result.namespace)
        self.assertEqual("search", result.method)
        self.assertEqual(
            {"album": "fire", "page": "1", "limit": "50"}, result.params
        )
        self.assertIsInstance(result, AlbumSearch)
        self.assertDictEqual(response["results"], actual)

        self.assertEqual(1, result.get_page())
        self.assertEqual(50, result.get_limit())
        self.assertEqual(661041, result.get_total())
        self.assertEqual(13221, result.get_total_pages())
        self.assertFalse(result.has_prev())
        self.assertTrue(result.has_next())
