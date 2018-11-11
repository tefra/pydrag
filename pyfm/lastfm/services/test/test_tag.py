from pyfm.lastfm.models import (
    TagInfo,
    TagSimilar,
    TagTopAlbums,
    TagTopArtists,
    TagTopTags,
    TagTopTracks,
    TagWeeklyChartList,
)
from pyfm.lastfm.services import TagService
from pyfm.lastfm.services.test import MethodTestCase, fixture


class TagServiceTests(MethodTestCase):
    def setUp(self):
        self.tag = TagService("rap")
        super(TagServiceTests, self).setUp()

    @fixture.use_cassette(path="tag/get_info")
    def test_get_info(self):
        result = self.tag.get_info(lang="en")
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_info", result.method)
        self.assertEqual({"lang": "en", "tag": "rap"}, result.params)
        self.assertIsInstance(result, TagInfo)
        self.assertDictEqual(response["tag"], actual)

    def test_get_info_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_info()

    @fixture.use_cassette(path="tag/get_similar")
    def test_get_similar(self):
        """
        @todo investigate why I cant get any results for this
        """
        self.tag.tag = "Disco"
        result = self.tag.get_similar()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_similar", result.method)
        self.assertEqual({"tag": "Disco"}, result.params)
        self.assertIsInstance(result, TagSimilar)
        self.assertDictEqual(response["similartags"], actual)

    def test_get_similar_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_similar()

    @fixture.use_cassette(path="tag/get_top_albums")
    def test_get_top_albums(self):
        result = self.tag.get_top_albums(page=1, limit=2)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_top_albums", result.method)
        self.assertEqual(
            {"limit": "2", "page": "1", "tag": "rap"}, result.params
        )
        self.assertGreater(len(result.album), 0)
        self.assertIsInstance(result, TagTopAlbums)
        self.assertDictEqual(response["albums"], actual)

    def test_get_top_albums_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_top_albums()

    @fixture.use_cassette(path="tag/get_top_artists")
    def test_get_top_artists(self):
        result = self.tag.get_top_artists(page=1, limit=2)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_top_artists", result.method)
        self.assertEqual(
            {"limit": "2", "page": "1", "tag": "rap"}, result.params
        )
        self.assertGreater(len(result.artist), 0)
        self.assertIsInstance(result, TagTopArtists)
        self.assertDictEqual(response["topartists"], actual)

    def test_get_top_artists_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_top_artists()

    @fixture.use_cassette(path="tag/get_top_tracks")
    def test_get_top_tracks(self):
        result = self.tag.get_top_tracks(page=1, limit=2)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_top_tracks", result.method)
        self.assertEqual(
            {"limit": "2", "page": "1", "tag": "rap"}, result.params
        )
        self.assertGreater(len(result.track), 0)
        self.assertIsInstance(result, TagTopTracks)
        self.assertDictEqual(response["tracks"], actual)

    def test_get_top_tracks_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_top_tracks()

    @fixture.use_cassette(path="tag/get_top_tags")
    def test_get_top_tags(self):
        result = self.tag.get_top_tags(page=2, limit=2)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_top_tags", result.method)
        self.assertEqual({"num_res": "2", "offset": "2"}, result.params)
        self.assertEqual(2, len(result.tag))
        self.assertIsInstance(result, TagTopTags)
        self.assertDictEqual(response["toptags"], actual)

    @fixture.use_cassette(path="tag/get_weekly_chart_list")
    def test_get_weekly_chart_list(self):
        result = self.tag.get_weekly_chart_list()
        actual = result.to_dict()
        response = result.response.json()["weeklychartlist"]

        self.assertEqual("Tag", result.namespace)
        self.assertEqual("get_weekly_chart_list", result.method)
        self.assertEqual({"tag": "rap"}, result.params)
        self.assertGreater(len(result.chart), 0)
        self.assertIsInstance(result, TagWeeklyChartList)
        self.assertDictEqual(response, actual)

        self.assertEqual(
            result.chart[0].from_date, response["chart"][0]["from"]
        )
        self.assertEqual(result.chart[0].to_date, response["chart"][0]["to"])

    def test_get_weekly_chart_list_no_tag(self):
        with self.assertRaises(AssertionError):
            TagService().get_weekly_chart_list()
