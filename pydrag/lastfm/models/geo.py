from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import Artist, Attributes, Track


@attrs(auto_attribs=True)
class GeoTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class GeoTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")
