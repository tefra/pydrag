from urllib.parse import urlencode

from attr import attrs

from pyfm.lastfm import config
from pyfm.lastfm.models import BaseModel


@attrs(auto_attribs=True)
class AuthToken(BaseModel):
    token: str

    @property
    def auth_url(self):
        params = dict(token=self.token, api_key=config.api_key)
        return "https://www.last.fm/api/auth?{}".format(urlencode(params))


@attrs(auto_attribs=True)
class AuthSession(BaseModel):
    key: str
    name: str
    subscriber: int
    token: str = None


@attrs(auto_attribs=True)
class AuthMobileSession(AuthSession):
    pass
