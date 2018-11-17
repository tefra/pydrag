from urllib.parse import urlencode

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm import config


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
