from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import Artist, Attributes


@attrs(auto_attribs=True)
class LibraryArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")
