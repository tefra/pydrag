from typing import List

from attr import attrs

from pydrag.core import BaseModel, mattrib
from pydrag.lastfm.models.common import (
    Artist,
    Artists,
    AttrModel,
    OpenSearch,
    Query,
    Tags,
    Wiki,
)


@attrs(auto_attribs=True)
class CorrectionArtist(AttrModel):
    artist: Artist


@attrs(auto_attribs=True)
class ArtistCorrection(BaseModel):
    correction: CorrectionArtist


@attrs(auto_attribs=True)
class ArtistInfo(Artist):
    tags: Tags = None
    bio: Wiki = None
    on_tour: int = mattrib("ontour", default=None)
    stats: Artist = None
    similar: Artists = None


@attrs(auto_attribs=True)
class ArtistMatches(BaseModel):
    artist: List[ArtistInfo]


@attrs(auto_attribs=True)
class ArtistSearch(OpenSearch):
    matches: ArtistMatches = mattrib("artistmatches")
    query: Query = mattrib("opensearch:Query")
