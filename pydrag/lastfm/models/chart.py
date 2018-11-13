from attr import attrs

from pydrag.lastfm.models.common import Artists, AttrModel, TagInfos, Tracks


@attrs(auto_attribs=True)
class ChartTopArtists(Artists, AttrModel):
    pass


@attrs(auto_attribs=True)
class ChartTopTracks(Tracks, AttrModel):
    pass


class ChartTopTags(TagInfos):
    pass
