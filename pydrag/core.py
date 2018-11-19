from abc import ABCMeta
from typing import Dict, TypeVar, Union
from urllib.parse import urlencode

import requests
from attr import asdict, attrib, fields
from cattr import structure
from requests import Response

from pydrag.lastfm import config

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
    def from_dict(cls, data: dict):
        return structure(data, cls)

    @staticmethod
    def _prepare(params: dict) -> dict:
        def cast(x):
            return str(int(x is True) if type(x) == bool else x)

        params = dict((k, cast(v)) for k, v in params.items() if v is not None)
        params.update(dict(format="json", api_key=config.api_key))
        return params

    @classmethod
    def retrieve(cls, bind=None, params={}) -> T:
        assert "method" in params
        if bind is None:
            bind = cls

        data = cls._prepare(params)
        url = "{}?{}".format(config.api_root_url, urlencode(data))
        response = requests.get(url)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        obj = cls._bind(bind, response, body)
        obj.params = params
        return obj

    @classmethod
    def _bind(cls, bind, resp: Response, body: Union[dict, list, None]) -> T:
        assert isinstance(body, dict)

        if body:
            data = body.get(next(iter(body.keys())))
            if isinstance(data, dict):
                obj = bind.from_dict(data)
            else:
                obj = bind(data)
        else:
            obj = bind()

        return obj


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
