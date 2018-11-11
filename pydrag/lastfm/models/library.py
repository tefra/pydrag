from typing import List

from attr import attrs
from pydrag.lastfm.models import Artist, Attributes, BaseModel, mattrib


@attrs(auto_attribs=True)
class LibraryArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")
