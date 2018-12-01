import os
from typing import Optional

from attr import dataclass, attrib

from pydrag.utils import md5


@dataclass(frozen=True)
class Config:
    api_key: str
    api_secret: str
    username: str
    password: str = attrib(converter=md5)
    api_root_url: str = "https://ws.audioscrobbler.com/2.0/"


config = None
try:
    """Attempt to create a config using environmental variables."""
    config = Config(
        api_key=os.environ["LASTFM_API_KEY"],
        api_secret=os.getenv("LASTFM_API_SECRET", ""),
        username=os.getenv("LASTFM_USERNAME", ""),
        password=os.getenv("LASTFM_PASSWORD", ""),
    )
except KeyError:
    pass


def configure(
    api_key: str,
    api_secret: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    global config
    config = Config(
        api_key=api_key,
        api_secret=api_secret or "",
        username=username or "",
        password=password or "",
    )


__all__ = ["config"]
