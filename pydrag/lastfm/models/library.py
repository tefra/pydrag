from attr import attrs

from pydrag.lastfm.models.common import Artists, AttrModel


@attrs(auto_attribs=True)
class LibraryArtists(Artists, AttrModel):
    pass
