from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.auth import AuthSession
from pydrag.models.auth import AuthToken
from pydrag.models.common import Config
from pydrag.models.track import Tag
from pydrag.models.track import Track
from pydrag.models.user import User
from pydrag.version import version

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    # tox -e docs doesn't load python-dotenv
    pass

configure = Config.instance

__all__ = [
    "User",
    "Track",
    "Album",
    "Artist",
    "Tag",
    "AuthToken",
    "AuthSession",
    "configure",
    "version",
]
