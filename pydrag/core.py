from abc import ABCMeta
from typing import Dict, TypeVar

from attr import asdict, attrib, fields
from cattr import structure
from requests import Response

T = TypeVar("T", bound="BaseModel")


class BaseModel(metaclass=ABCMeta):
    signed: bool = attrib(init=False)
    auth: bool = attrib(init=False)
    stateful: bool = attrib(init=False)
    namespace: str = attrib(init=False)
    method: str = attrib(init=False)
    http_method: str = attrib(init=False)
    params: dict = attrib(init=False)
    response: Response = attrib(init=False)

    def to_dict(self: T) -> Dict:
        return asdict(self, filter=lambda f, v: v is not None)

    def get_fields(self):
        return fields(self)

    @classmethod
    def from_dict(cls: T, data: dict) -> T:
        return structure(data, cls)


def pythonic_variables(data):
    map = {
        "albummatches": "matches",
        "artistmatches": "matches",
        "trackmatches": "matches",
        "opensearch:Query": "query",
        "perPage": "limit",
        "totalPages": "total_pages",
        "startPage": "page",
        "trackcorrected": "track_corrected",
        "artistcorrected": "artist_corrected",
        "to": "to_date",
        "for": "user",
        "from": "from_date",
        "tagcount": "tag_count",
        "@attr": "attr",
        "#text": "text",
        "unixtime": "timestamp",
        "uts": "timestamp",
        "searchTerms": "search_terms",
        "opensearch:itemsPerPage": "limit",
        "opensearch:startIndex": "offset",
        "opensearch:totalResults": "total",
        "toptags": "top_tags",
        "ignoredMessage": "ignored_message",
        "albumArtist": "album_artist",
        "streamId": "stream_id",
        "albumArtist": "album_artist",
        "scrobblesource": "source",
        "realname": "real_name",
        "recenttrack": "recent_track",
        "recenttrack": "recent_track",
        "ontour": "on_tour",
        "num_res": "limit",
    }

    return {map.get(key, key): value for key, value in data}
