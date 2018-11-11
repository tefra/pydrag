from typing import List

from attr import attrs

from pyfm.lastfm.models import Attributes, Artist, Track, mattrib, BaseModel


@attrs(auto_attribs=True)
class GeoTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class GeoTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")
