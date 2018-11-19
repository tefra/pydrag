from urllib.parse import urlencode

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm import api, config
from pydrag.lastfm.api import POST


@dataclass
class AuthToken(BaseModel):
    token: str

    @property
    def auth_url(self):
        params = dict(token=self.token, api_key=config.api_key)
        return "https://www.last.fm/api/auth?{}".format(urlencode(params))


@dataclass
class AuthSession(BaseModel):
    key: str
    name: str
    subscriber: int
    token: str = None


class AuthMobileSession(AuthSession):
    pass


class AuthService:
    @api.operation(signed=False)
    def get_token(self) -> AuthToken:
        """
        Fetch an unathorized request token for an API account. Open the
        AuthToken.auth_url where the user must authorize the token use the
        get_session with the same authorized token to retrieve the use session.

        :returns: AuthToken
        """
        return None

    @api.operation(method=POST, signed=True)
    def get_session(self, token: str) -> AuthSession:
        return dict(token=token)

    @api.operation(method=POST, signed=True, auth=True)
    def get_mobile_session(self) -> AuthMobileSession:
        """
        Create a web service session for a user. Used for authenticating a user
        when the password can be inputted by the user. Accepts email address as
        well, so please use the username supplied in the output.

        :returns: AuthMobileSession
        """
        return None
