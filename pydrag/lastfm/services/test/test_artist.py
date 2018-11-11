from pydrag.lastfm.models import (
    ArtistCorrection,
    ArtistInfo,
    ArtistSearch,
    ArtistSimilar,
    ArtistTags,
    ArtistTopTags,
    ArtistTopTracks,
    BaseModel,
)
from pydrag.lastfm.services import ArtistService
from pydrag.lastfm.services.test import MethodTestCase, fixture


class ArtistServiceTests(MethodTestCase):
    def setUp(self):
        self.artist = ArtistService(
            artist="Guns N' Roses", mbid="eeb1195b-f213-4ce1-b28c-8565211f8e43"
        )
        super(ArtistServiceTests, self).setUp()

    @fixture.use_cassette(path="artist/add_tags")
    def test_add_tags(self):
        result = self.artist.add_tags(["foo", "bar"])
        self.assertDictEqual(
            {"artist": "Guns N' Roses", "sk": "CENSORED", "tags": "foo,bar"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="artist/get_tags")
    def test_get_tags(self):
        # todo check all these list retrievals that work without data
        result = self.artist.get_tags(user="Zaratoustre")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_tags", result.method)
        self.assertDictEqual(
            {
                "artist": "Guns N' Roses",
                "autocorrect": True,
                "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
                "user": "Zaratoustre",
            },
            result.params,
        )
        self.assertIsInstance(result, ArtistTags)
        self.assertEqual(2, len(result.tag))
        self.assertDictEqual(response["tags"], actual)

    @fixture.use_cassette(path="artist/remove_tag")
    def test_remove_tag(self):
        result = self.artist.remove_tag("bar")
        self.assertDictEqual(
            {"artist": "Guns N' Roses", "sk": "CENSORED", "tag": "bar"},
            result.params,
        )
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="artist/get_info")
    def test_get_info(self):
        self.artist.artist = None
        result = self.artist.get_info()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertEqual(
            {
                "autocorrect": True,
                "lang": "en",
                "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            },
            result.params,
        )
        self.assertIsInstance(result, ArtistInfo)
        self.assertDictEqual(response["artist"], actual)

    @fixture.use_cassette(path="artist/get_correction")
    def test_get_correction(self):
        self.artist.mbid = None
        self.artist.artist = "Guns an roses"
        result = self.artist.get_correction()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_correction", result.method)
        self.assertEqual({"artist": "Guns an roses"}, result.params)
        self.assertIsInstance(result, ArtistCorrection)
        self.assertDictEqual(response["corrections"], actual)

    @fixture.use_cassette(path="artist/get_top_tags")
    def test_get_top_tags(self):
        result = self.artist.get_top_tags(True)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual(
            {
                "artist": "Guns N' Roses",
                "autocorrect": True,
                "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            },
            result.params,
        )
        self.assertGreater(len(result.tag), 0)
        self.assertIsInstance(result, ArtistTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="artist/search")
    def test_search(self):
        self.artist.artist = "gun"
        result = self.artist.search()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("search", result.method)
        self.assertEqual(
            {"artist": "gun", "page": "1", "limit": "50"}, result.params
        )

        self.assertGreater(len(result.artistmatches.artist), 0)
        self.assertIsInstance(result, ArtistSearch)
        self.assertDictEqual(response["results"], actual)

    @fixture.use_cassette(path="artist/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.artist.get_top_tracks(True)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_top_tracks", result.method)
        self.assertEqual(
            {
                "artist": "Guns N' Roses",
                "autocorrect": True,
                "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
                "page": 1,
                "limit": 50,
            },
            result.params,
        )
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, ArtistTopTracks)
        self.assertDictEqual(response["toptracks"], actual)

    @fixture.use_cassette(path="artist/get_similar")
    def test_get_similar(self):
        result = self.artist.get_similar(True)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_similar", result.method)
        self.assertEqual(
            {
                "artist": "Guns N' Roses",
                "autocorrect": True,
                "limit": 50,
                "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            },
            result.params,
        )
        self.assertGreater(len(result.artist), 0)
        self.assertIsInstance(result, ArtistSimilar)
        self.assertDictEqual(response["similarartists"], actual)
