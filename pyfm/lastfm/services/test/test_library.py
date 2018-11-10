from pyfm.lastfm.methods import Library
from pyfm.lastfm.models import LibraryArtists
from pyfm.lastfm.methods.test import fixture, MethodTestCase


class LibraryTests(MethodTestCase):
    def setUp(self):
        self.library = Library("rj")
        super(LibraryTests, self).setUp()

    @fixture.use_cassette(path="library/get_artists")
    def test_get_artists(self):
        result = self.library.get_artists()
        actual = result.to_dict()
        response = result.response.json()

        self.assertIsInstance(result, LibraryArtists)
        self.assertDictEqual(response["artists"], actual)
