from pydrag.lastfm.models.auth import AuthSession
from pydrag.lastfm.models.test import MethodTestCase, fixture


class AuthSessionTests(MethodTestCase):
    @fixture.use_cassette(path="auth/get_mobile_session")
    def test_get_mobile_session(self):
        result = AuthSession.get()
        expected_params = {"method": "auth.getMobileSession"}

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, AuthSession)
        self.assertFixtureEqual("auth/get_mobile_session", result.to_dict())
