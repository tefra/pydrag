from pydrag.lastfm.models import ChartTopArtists, ChartTopTags, ChartTopTracks
from pydrag.lastfm.services import ChartService
from pydrag.lastfm.services.test import MethodTestCase, fixture


class ChartServiceTests(MethodTestCase):
    def setUp(self):
        self.chart = ChartService(page=2, limit=10)
        super(ChartServiceTests, self).setUp()

    @fixture.use_cassette(path="chart/get_top_artists")
    def test_get_top_artists(self):
        result = self.chart.get_top_artists()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Chart", result.namespace)
        self.assertEqual("get_top_artists", result.method)
        self.assertEqual({"limit": "10", "page": "2"}, result.params)
        self.assertIsInstance(result, ChartTopArtists)
        self.assertGreater(len(result.artist), 0)
        self.assertDictEqual(response["artists"], actual)

    @fixture.use_cassette(path="chart/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.chart.get_top_tracks()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Chart", result.namespace)
        self.assertEqual("get_top_tracks", result.method)
        self.assertEqual({"limit": "10", "page": "2"}, result.params)
        self.assertIsInstance(result, ChartTopTracks)
        self.assertGreater(len(result.track), 0)
        self.assertDictEqual(response["tracks"], actual)

    @fixture.use_cassette(path="chart/get_top_tags")
    def test_get_top_tags(self):
        result = self.chart.get_top_tags()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Chart", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual({"limit": "10", "page": "2"}, result.params)
        self.assertIsInstance(result, ChartTopTags)
        self.assertGreater(len(result.tag), 0)
        self.assertDictEqual(response["tags"], actual)
