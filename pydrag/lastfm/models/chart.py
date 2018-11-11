from typing import List

from attr import attrs
from pydrag.lastfm.models import (
    Artist,
    Attributes,
    BaseModel,
    TagInfo,
    Track,
    mattrib,
)


@attrs(auto_attribs=True)
class ChartTopArtists(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class ChartTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class ChartTopTags(BaseModel):
    tag: List[TagInfo]
    attr: Attributes = mattrib("@attr")
