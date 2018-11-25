import os

from attr import attrib, dataclass

from pydrag.lastfm.utils import md5


@dataclass(frozen=True)
class Config:
    api_key: str
    api_secret: str
    username: str
    password: str = attrib(converter=lambda x: not x or md5(x))
    api_root_url: str = "https://ws.audioscrobbler.com/2.0/"


config = Config(
    api_key=os.getenv("LASTFM_API_KEY"),
    api_secret=os.getenv("LASTFM_API_SECRET"),
    username=os.getenv("LASTFM_USERNAME"),
    password=os.getenv("LASTFM_PASSWORD"),
)
