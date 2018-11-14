from pydrag.lastfm.models.common import ArtistList
from pydrag.lastfm.services.library import LibraryService
from pydrag.lastfm.services.test import MethodTestCase, fixture


class LibraryServiceTests(MethodTestCase):
    def setUp(self):
        self.library = LibraryService("rj")
        super(LibraryServiceTests, self).setUp()

    @fixture.use_cassette(path="library/get_artists")
    def test_get_artists(self):
        result = self.library.get_artists()
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, ArtistList)
        self.assertDictEqual(response["artists"], actual)
