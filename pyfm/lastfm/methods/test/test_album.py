from unittest import skip

from lastfm.models import AlbumTopTags, AlbumInfo, AlbumTags, AlbumSearch
from pyfm.lastfm.methods.album import Album
from pyfm.lastfm.methods.test import fixture, MethodTestCase


class AlbumTests(MethodTestCase):
    def setUp(self):
        self.album = Album(
            album="A Night at the Opera",
            artist="Queen",
            mbid="6defd963-fe91-4550-b18e-82c685603c2b",
        )
        super(AlbumTests, self).setUp()

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
                "autocorrect": "1",
                "lang": "en",
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
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
                "autocorrect": "0",
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertGreater(len(result.tag), 0)
        self.assertIsInstance(result, AlbumTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @skip("Need data")
    @fixture.use_cassette(path="album/get_tags")
    def test_get_tags(self):
        result = self.album.get_tags(user="RJ")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Album", result.namespace)
        self.assertEqual("get_tags", result.method)
        self.assertEqual(
            {
                "album": "A Night at the Opera",
                "artist": "Queen",
                "autocorrect": "1",
                "mbid": "6defd963-fe91-4550-b18e-82c685603c2b",
                "user": "RJ",
            },
            result.params,
        )
        self.assertIsNone(None, result.data)
        self.assertIsInstance(result, AlbumTags)
        self.assertDictEqual(response["tags"], actual)

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
        self.assertIsNone(None, result.data)
        self.assertIsInstance(result, AlbumSearch)
        self.assertDictEqual(response["results"], actual)
