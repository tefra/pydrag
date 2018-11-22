from pydrag.core import BaseModel
from pydrag.lastfm.models.artist import Artist, ArtistCorrection, ArtistSearch
from pydrag.lastfm.models.common import ArtistList, TagList, TrackList
from pydrag.lastfm.models.test import MethodTestCase, fixture


class ArtistServiceTests(MethodTestCase):
    def setUp(self):
        self.artist = Artist(
            name="Guns N' Roses", mbid="eeb1195b-f213-4ce1-b28c-8565211f8e43"
        )
        super(ArtistServiceTests, self).setUp()

    @fixture.use_cassette(path="artist/add_tags")
    def test_add_tags(self):
        result = self.artist.add_tags(["foo", "bar"])
        expected_params = {
            "arist": "Guns N' Roses",
            "method": "artist.addTags",
            "tags": "foo,bar",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="artist/get_tags")
    def test_get_tags(self):
        result = self.artist.get_tags(user="Zaratoustre")
        expected_params = {
            "artist": "Guns N' Roses",
            "autocorrect": True,
            "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            "method": "artist.getTags",
            "user": "Zaratoustre",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("artist/get_tags", result.to_dict())

    @fixture.use_cassette(path="artist/remove_tag")
    def test_remove_tag(self):
        result = self.artist.remove_tag("bar")
        expected_params = {
            "arist": "Guns N' Roses",
            "method": "artist.removeTag",
            "tag": "bar",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseModel)

    @fixture.use_cassette(path="artist/find")
    def test_find(self):
        self.artist.artist = None
        result = Artist.find("Guns N' Roses")
        expected_params = {
            "artist": "Guns N' Roses",
            "autocorrect": True,
            "lang": "en",
            "method": "artist.getInfo",
            "username": None,
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, Artist)
        self.assertFixtureEqual("artist/find", result.to_dict())

    @fixture.use_cassette(path="artist/get_correction")
    def test_get_correction(self):
        self.artist.mbid = None
        self.artist.name = "Guns an roses"
        result = self.artist.get_correction()
        expected_params = {
            "artist": "Guns an roses",
            "method": "artist.getCorrection",
        }
        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, ArtistCorrection)
        self.assertFixtureEqual("artist/get_correction", result.to_dict())

    @fixture.use_cassette(path="artist/get_top_tags")
    def test_get_top_tags(self):
        result = self.artist.get_top_tags()
        expected_params = {
            "artist": "Guns N' Roses",
            "autocorrect": True,
            "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            "method": "artist.getTopTags",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, TagList)
        self.assertFixtureEqual("artist/get_top_tags", result.to_dict())

    @fixture.use_cassette(path="artist/search")
    def test_search(self):
        result = Artist.search("gun")
        expected_params = {
            "artist": "gun",
            "limit": 50,
            "method": "artist.search",
            "page": 1,
        }
        self.assertEqual(expected_params, result.params)
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
        result = self.artist.get_top_tracks()
        expected_params = {
            "artist": "Guns N' Roses",
            "autocorrect": True,
            "limit": 50,
            "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            "method": "artist.getTopTracks",
            "page": 1,
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, TrackList)
        self.assertFixtureEqual("artist/get_top_tracks", result.to_dict())

    @fixture.use_cassette(path="artist/get_similar")
    def test_get_similar(self):
        result = self.artist.get_similar()
        expected_params = {
            "artist": "Guns N' Roses",
            "autocorrect": True,
            "limit": 50,
            "mbid": "eeb1195b-f213-4ce1-b28c-8565211f8e43",
            "method": "artist.getSimilar",
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, ArtistList)
        self.assertFixtureEqual("artist/get_similar", result.to_dict())
