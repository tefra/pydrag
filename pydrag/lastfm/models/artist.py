from typing import List

from attr import attrs
from pydrag.lastfm.models import (
    Artist,
    Attributes,
    BaseModel,
    Query,
    Tags,
    TagsAttr,
    Track,
    Wiki,
    mattrib,
)


@attrs(auto_attribs=True)
class ArtistTags(TagsAttr):
    pass


@attrs(auto_attribs=True)
class ArtistTopTags(TagsAttr):
    pass


@attrs(auto_attribs=True)
class SimilarArtist(BaseModel):
    artist: List[Artist]


@attrs(auto_attribs=True)
class ArtistInfo(Artist):
    tags: Tags = None
    bio: Wiki = None
    ontour: int = None
    stats: Artist = None
    similar: SimilarArtist = None


@attrs(auto_attribs=True)
class CorrectionArtist(BaseModel):
    artist: Artist
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class ArtistCorrection(BaseModel):
    correction: CorrectionArtist


@attrs(auto_attribs=True)
class ArtistMatches(BaseModel):
    artist: List[ArtistInfo]


@attrs(auto_attribs=True)
class ArtistSearch(BaseModel):
    artistmatches: ArtistMatches
    query: Query = mattrib("opensearch:Query")
    itemsPerPage: int = mattrib("opensearch:itemsPerPage")
    startIndex: int = mattrib("opensearch:startIndex")
    totalResults: int = mattrib("opensearch:totalResults")
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class ArtistTopTracks(BaseModel):
    track: List[Track]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class ArtistSimilar(BaseModel):
    artist: List[Artist]
    attr: Attributes = mattrib("@attr")
