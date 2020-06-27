from pydrag import Config
from pydrag.models.auth import AuthSession
from pydrag.models.auth import AuthToken
from tests import fixture
from tests import MethodTestCase


class AuthSessionTests(MethodTestCase):
    @fixture.use_cassette(path="auth/get_mobile_session")
    def test_authenticate(self):
        result = AuthSession.authenticate()
        expected_params = {"method": "auth.getMobileSession"}

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, AuthSession)
        self.assertFixtureEqual("auth/get_mobile_session", result.to_dict())

    @fixture.use_cassette(path="auth/get_session")
    def test_get_session(self):
        token = "authenticated_token"
        result = AuthSession.from_token(token)

        expected_params = {
            "method": "auth.getSession",
            "token": "authenticated_token",
        }

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, AuthSession)
        self.assertFixtureEqual("auth/get_session", result.to_dict())


class AuthTokenTests(MethodTestCase):
    @fixture.use_cassette(path="auth/get_token")
    def test_generate(self):
        Config.instance().api_key = "abc"
        result = AuthToken.generate()
        expected_params = {"method": "auth.getToken"}

        self.assertDictEqual(expected_params, result.params)
        self.assertIsInstance(result, AuthToken)

        auth_url = "https://www.last.fm/api/auth?token=CENSORED&api_key=abc"
        self.assertEqual(auth_url, result.auth_url)
        self.assertFixtureEqual("auth/get_token", result.to_dict())
