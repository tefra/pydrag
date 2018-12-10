from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.common import Config
from pydrag.models.track import Tag
from pydrag.models.track import Track
from pydrag.models.user import User
from pydrag.models.auth import AuthToken, AuthSession


try:
    import dotenv
except ImportError:
    # tox doesn't load python-dotenv
    pass
else:
    dotenv.load_dotenv()

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
]
