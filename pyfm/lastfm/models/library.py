from typing import List

from attr import attrs

from lastfm.models import Attributes, Artist, mattrib
from pyfm import BaseModel


@attrs(auto_attribs=True)
class LibraryArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")
