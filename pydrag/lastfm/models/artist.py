from typing import List

from attr import dataclass

from pydrag.core import BaseModel
from pydrag.lastfm.models.common import (
    Artist,
    Artists,
    AttrModel,
    OpenSearch,
    Query,
    Tags,
    Wiki,
)


@dataclass
class CorrectionArtist(AttrModel):
    artist: Artist


@dataclass
class ArtistCorrection(BaseModel):
    correction: CorrectionArtist


@dataclass
class ArtistInfo(Artist):
    tags: Tags = None
    bio: Wiki = None
    on_tour: int = None
    stats: Artist = None
    similar: Artists = None


@dataclass
class ArtistMatches(BaseModel):
    artist: List[ArtistInfo]


@dataclass
class ArtistSearch(OpenSearch):
    matches: ArtistMatches
    query: Query
