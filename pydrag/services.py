from typing import Dict, Optional, Type
from urllib.parse import urlencode

import requests

from pydrag.exceptions import ApiError
from pydrag.models.common import BaseModel, ListModel
from pydrag.models.config import config
from pydrag.utils import md5


class ApiMixin:
    @classmethod
    def retrieve(cls, bind, many=None, params={}):
        data = cls.prepare_params(params)
        url = "{}?{}".format(config.api_root_url, urlencode(data))
        response = requests.get(url)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        cls.raise_for_error(body)
        obj = cls.bind_data(bind, body, many)
        obj.params = params
        return obj

    @classmethod
    def submit(
        cls, bind, many=None, stateful=False, authenticate=False, params={}
    ):
        data = cls.prepare_params(params)
        if authenticate:
            data.update(
                dict(
                    username=config.username,
                    authToken=md5(str(config.username) + str(config.password)),
                )
            )

        if stateful:
            from pydrag.models.auth import AuthSession

            session = AuthSession.get()
            data.update({"sk": session.key})

        if authenticate or "sk" in data:
            data.update({"api_sig": cls.sign(data)})

        url = config.api_root_url
        response = requests.post(url, data=data)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        cls.raise_for_error(body)
        obj = cls.bind_data(bind, body, many)
        obj.params = params
        return obj

    @staticmethod
    def prepare_params(params: dict) -> dict:
        def cast(x):
            return str(int(x is True) if type(x) == bool else x)

        params = dict((k, cast(v)) for k, v in params.items() if v is not None)
        params.update(dict(format="json", api_key=config.api_key))
        return params

    @classmethod
    def bind_data(
        cls,
        bind: Type[BaseModel],
        body: Optional[Dict],
        many: Optional[str] = None,
    ):
        if not body:
            return bind()

        data = body[next(iter(body.keys()))]
        if many is None:
            return bind.from_dict(data)

        for m in many.split("."):
            data = data.pop(m)

        if isinstance(data, dict):
            data = [data]

        return ListModel(data=[bind.from_dict(d) for d in data])

    @staticmethod
    def raise_for_error(body: dict):
        if "error" in body:
            raise ApiError(**body)

    @staticmethod
    def sign(params):
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [str(k) + str(params[k]) for k in keys if params.get(k)]
        signature.append(str(config.api_secret))
        return md5("".join(signature))


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
