from typing import List

from attr import attrs

from pyfm import BaseModel, mattrib
from pyfm.lastfm.models import Attributes, Artist, Wiki, Tag, Track, Query


@attrs(auto_attribs=True)
class ArtistTopTags(BaseModel):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tags(BaseModel):
    tag: List[Tag] = None


@attrs(auto_attribs=True)
class ArtistTags(Tags):
    tag: List[Tag]
    attr: Attributes = mattrib("@attr")


@attrs(auto_attribs=True)
class Tracks(BaseModel):
    track: List[Track] = None


@attrs(auto_attribs=True)
class SimilarArtist(BaseModel):
    artist: List[Artist]


@attrs(auto_attribs=True)
class ArtistStat(BaseModel):
    listeners: int
    playcount: int


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
