from attr import attrs

from pydrag.lastfm.models.common import Artists, AttrModel, Tracks


@attrs(auto_attribs=True)
class GeoTopArtists(Artists, AttrModel):
    pass


@attrs(auto_attribs=True)
class GeoTopTracks(Tracks, AttrModel):
    pass
