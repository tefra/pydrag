import os
from typing import Optional

from attr import attrib, dataclass

from pydrag.utils import md5


@dataclass
class Config:
    api_key: str
    api_secret: str
    username: str
    password: str = attrib(converter=md5)
    api_url: str = "https://ws.audioscrobbler.com/2.0/"

    @property
    def auth_token(self):
        return md5(str(self.username) + str(self.password))


config = Config(
    api_key=os.getenv("LASTFM_API_KEY", ""),
    api_secret=os.getenv("LASTFM_API_SECRET", ""),
    username=os.getenv("LASTFM_USERNAME", ""),
    password=os.getenv("LASTFM_PASSWORD", ""),
)


def configure(
    api_key: str,
    api_secret: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    config.api_key = api_key
    config.api_secret = api_secret or ""
    config.username = username or ""
    config.password = password or ""
