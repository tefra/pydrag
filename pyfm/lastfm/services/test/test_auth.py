from pyfm.lastfm.methods import Auth
from pyfm.lastfm.methods.test import MethodTestCase, fixture
from pyfm.lastfm.models import AuthToken, AuthMobileSession, AuthSession


class AuthTests(MethodTestCase):
    def setUp(self):
        self.auth = Auth()

    @fixture.use_cassette(path="auth/get_token")
    def test_get_token(self):
        result = self.auth.get_token()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Auth", result.namespace)
        self.assertEqual("get_token", result.method)
        self.assertEqual({}, result.params)
        self.assertIsInstance(result, AuthToken)
        self.assertIsNotNone(result.auth_url)
        self.assertIsNotNone(result.token)
        self.assertDictEqual(response, actual)

    @fixture.use_cassette(path="auth/get_session")
    def test_get_session(self):
        auth = Auth().get_token()

        # Manually grand access to the request token open the auth url
        # print (auth.auth_url)
        # import time; time.sleep(15)

        result = self.auth.get_session(auth.token)
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Auth", result.namespace)
        self.assertEqual("get_session", result.method)
        self.assertEqual(dict(token=auth.token), result.params)
        self.assertIsInstance(result, AuthSession)
        self.assertDictEqual(response["session"], actual)

    @fixture.use_cassette(path="auth/get_mobile_session")
    def test_get_mobile_session(self):
        result = self.auth.get_mobile_session()
        actual = result.to_dict()
        response = result.response.json()

        self.assertEqual("Auth", result.namespace)
        self.assertEqual("get_mobile_session", result.method)
        self.assertIsInstance(result, AuthMobileSession)
        self.assertDictEqual(response["session"], actual)
