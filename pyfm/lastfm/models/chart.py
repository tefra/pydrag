from typing import List

from attr import attrs

from lastfm.models import Attributes, Artist, Track, TagInfo
from pyfm import BaseModel


@attrs(auto_attribs=True)
class ChartTopArtists(BaseModel):
    attr: Attributes
    artist: List[Artist]


@attrs(auto_attribs=True)
class ChartTopTracks(BaseModel):
    attr: Attributes
    track: List[Track]


@attrs(auto_attribs=True)
class ChartTopTags(BaseModel):
    tag: List[TagInfo]
    attr: Attributes
