from attr import attrs

from pydrag.lastfm.models.common import (
    Albums,
    Artists,
    AttrModel,
    Charts,
    TagInfos,
    Tracks,
)


class TagSimilar(TagInfos):
    pass


class TagTopTags(TagInfos):
    pass


@attrs(auto_attribs=True)
class TagTopAlbums(Albums, AttrModel):
    pass


@attrs(auto_attribs=True)
class TagTopArtists(Artists, AttrModel):
    pass


@attrs(auto_attribs=True)
class TagTopTracks(Tracks, AttrModel):
    pass


@attrs(auto_attribs=True)
class TagWeeklyChartList(Charts, AttrModel):
    pass
