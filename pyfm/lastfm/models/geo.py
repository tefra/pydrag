from typing import List

from attr import attrs

from lastfm.models import Attributes, Artist, Track
from pyfm import BaseModel


@attrs(auto_attribs=True)
class GeoTopArtists(BaseModel):
    attr: Attributes
    artist: List[Artist]


@attrs(auto_attribs=True)
class GeoTopTracks(BaseModel):
    attr: Attributes
    track: List[Track]
