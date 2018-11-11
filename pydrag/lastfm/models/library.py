from typing import List

from attr import attrs

from pyfm.lastfm.models import Attributes, Artist, mattrib, BaseModel


@attrs(auto_attribs=True)
class LibraryArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")
