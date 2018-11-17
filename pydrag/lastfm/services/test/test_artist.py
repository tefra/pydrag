from pydrag.core import BaseModel
from pydrag.lastfm.models.artist import (
    ArtistCorrection,
    ArtistInfo,
    ArtistSearch,
)
from pydrag.lastfm.models.common import ArtistList, TagList, TrackList
from pydrag.lastfm.services.artist import ArtistService
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
        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("artist/get_tags", result.to_dict())

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
        self.assertFixtureEqual("artist/get_info", result.to_dict())

    @fixture.use_cassette(path="artist/get_correction")
    def test_get_correction(self):
        self.artist.mbid = None
        self.artist.artist = "Guns an roses"
        result = self.artist.get_correction()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("get_correction", result.method)
        self.assertEqual({"artist": "Guns an roses"}, result.params)
        self.assertIsInstance(result, ArtistCorrection)
        self.assertFixtureEqual("artist/get_correction", result.to_dict())

    @fixture.use_cassette(path="artist/get_top_tags")
    def test_get_top_tags(self):
        result = self.artist.get_top_tags(True)

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

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("artist/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="artist/search")
    def test_search(self):
        self.artist.artist = "gun"
        result = self.artist.search()

        self.assertEqual("Artist", result.namespace)
        self.assertEqual("search", result.method)
        self.assertEqual(
            {"artist": "gun", "page": 1, "limit": 50}, result.params
        )

        self.assertIsInstance(result, ArtistSearch)
        self.assertFixtureEqual("artist/search", result.to_dict())

        self.assertEqual(1, result.get_page())
        self.assertEqual(50, result.get_limit())
        self.assertEqual(101477, result.get_total())
        self.assertEqual(2030, result.get_total_pages())
        self.assertFalse(result.has_prev())
        self.assertTrue(result.has_next())

    @fixture.use_cassette(path="artist/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.artist.get_top_tracks(True)

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

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual("artist/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="artist/get_similar")
    def test_get_similar(self):
        result = self.artist.get_similar(True)

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

        self.assertIsInstance(result, ArtistList)
        self.assertFixtureEqual("artist/get_similar", result.to_dict())
