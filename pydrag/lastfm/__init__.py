import os
from enum import Enum

from attr import dataclass, ib

from pydrag.lastfm.utils import md5


@dataclass(frozen=True)
class Config:
    api_key: str
    api_secret: str
    username: str
    password: str = ib(converter=lambda x: not x or md5(x))
    api_root_url: str = "https://ws.audioscrobbler.com/2.0/"


config = Config(
    api_key=os.getenv("LASTFM_API_KEY"),
    api_secret=os.getenv("LASTFM_API_SECRET"),
    username=os.getenv("LASTFM_USERNAME"),
    password=os.getenv("LASTFM_PASSWORD"),
)

GET = "get"
POST = "post"


class Period(Enum):
    overall = "overall"
    week = "7day"
    month = "1month"
    quarter = "3month"
    semester = "6month"
    year = "12month"
