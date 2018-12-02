from pydrag.core import BaseListModel, BaseModel
from pydrag.lastfm.models.artist import Artist, ArtistMini
from pydrag.lastfm.models.test import MethodTestCase, fixture


class ArtistTests(MethodTestCase):
    def setUp(self):
        self.artist = Artist(
            name="Guns N' Roses", mbid="eeb1195b-f213-4ce1-b28c-8565211f8e43"
        )
        super(ArtistTests, self).setUp()

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
        self.assertIsInstance(result, BaseListModel)
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
        self.assertIsInstance(result, ArtistMini)
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

        self.assertIsInstance(result, BaseListModel)
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
        self.assertIsInstance(result, BaseListModel)
        self.assertFixtureEqual("artist/search", result.to_dict())

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

        self.assertIsInstance(result, BaseListModel)
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

        self.assertIsInstance(result, BaseListModel)
        self.assertFixtureEqual("artist/get_similar", result.to_dict())

    @fixture.use_cassette(path="geo/get_top_artists")
    def test_get_top_tracks_by_country(self):
        result = Artist.get_top_artists_by_country(
            country="greece", page=1, limit=10
        )

        expected_params = {
            "country": "greece",
            "limit": 10,
            "method": "geo.getTopArtists",
            "page": 1,
        }
        self.assertEqual(expected_params, result.params)

        self.assertIsInstance(result, BaseListModel)

        self.assertFixtureEqual("geo/get_top_artists", result.to_dict())

    @fixture.use_cassette(path="chart/get_top_artists")
    def test_get_top_artists_chart(self):
        result = Artist.get_top_artists_chart(limit=10, page=2)
        expected_params = {
            "limit": 10,
            "method": "chart.getTopArtists",
            "page": 2,
        }

        self.assertEqual(expected_params, result.params)
        self.assertIsInstance(result, BaseListModel)
        self.assertFixtureEqual("chart/get_top_artists", result.to_dict())
