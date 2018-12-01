from abc import ABCMeta
from collections import UserList
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from urllib.parse import urlencode

import requests
from attr import asdict, attrib, dataclass, fields
from cattr import structure
from requests import Response

from pydrag.lastfm import config
from pydrag.utils import md5

T = TypeVar("T", bound="BaseModel")
TL = TypeVar("TL", bound="BaseListModel")


class BaseModel(metaclass=ABCMeta):
    params: Optional[dict] = attrib(init=False)
    response: Optional[Response] = attrib(init=False)

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
    def retrieve(cls, bind=None, many=None, params={}) -> Union[T, TL]:
        assert "method" in params
        if bind is None:
            bind = cls

        data = cls._prepare(params)
        url = "{}?{}".format(config.api_root_url, urlencode(data))
        response = requests.get(url)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        obj: Union[T, TL] = cls._bind(bind, body, many)
        obj.params = params
        return obj

    @classmethod
    def submit(
        cls, bind=None, stateful=False, authenticate=False, params={}
    ) -> Union[T, TL]:
        assert "method" in params
        if bind is None:
            bind = cls

        data = cls._prepare(params)
        if authenticate:
            data.update(
                dict(
                    username=config.username,
                    authToken=md5(str(config.username) + str(config.password)),
                )
            )

        if stateful:
            from pydrag.lastfm.models.auth import AuthSession

            session = AuthSession.get()
            data.update({"sk": session.key})

        if authenticate or "sk" in data:
            data.update({"api_sig": cls.sign(data)})

        url = config.api_root_url
        response = requests.post(url, data=data)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        obj: Union[T, TL] = cls._bind(bind, body)
        obj.params = params
        return obj

    @classmethod
    def _bind(
        cls, bind: Type, body: Any, many: Union[str, tuple] = None
    ) -> Union[T, TL]:
        assert isinstance(body, dict)

        if body:
            data = body.get(next(iter(body.keys())))
            if isinstance(data, dict):
                if many:
                    if isinstance(many, str):
                        many = (many,)

                    try:
                        for m in many:
                            data = data.pop(m)
                        items = [bind.from_dict(d) for d in data]
                    except KeyError:
                        items = []

                    obj = BaseListModel(data=items)
                else:
                    obj = bind.from_dict(data)
            else:
                obj = bind(data)
        else:
            obj = bind()

        return obj  # type: ignore

    @staticmethod
    def sign(params):
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [str(k) + str(params[k]) for k in keys if params.get(k)]
        signature.append(str(config.api_secret))
        return md5("".join(signature))


@dataclass(cmp=False)
class BaseListModel(UserList):
    data: List[BaseModel] = []
    params: Optional[dict] = attrib(init=False)
    response: Optional[Response] = attrib(init=False)

    def to_dict(self) -> Dict:
        """

        :return:
        :rtype:
        """
        return dict(data=[item.to_dict() for item in self])


def pythonic_variables(data):
    map = {
        "albummatches": "albums",
        "artistmatches": "artists",
        "trackmatches": "tracks",
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
        "realname": "real_name",
        "recenttrack": "recent_track",
        "recenttrack": "recent_track",
        "ontour": "on_tour",
        "num_res": "limit",
        "title": "name",
    }

    """
    A list of fields that dont make make sense in the api responses
    Either they don't always have the same value type or have a dev message
    """
    fixme = ["subscriber", "type", "scrobblesource", "bootstrap", "streamable"]

    return {map.get(k, k): v for k, v in data if k not in fixme}
