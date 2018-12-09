from pydrag.models.album import Album
from pydrag.models.artist import Artist
from pydrag.models.common import Config
from pydrag.models.track import Tag
from pydrag.models.track import Track
from pydrag.models.user import User

configure = Config.instance

__all__ = ["User", "Track", "Album", "Artist", "Tag", "configure"]
