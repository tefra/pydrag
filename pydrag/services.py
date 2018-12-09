from typing import Dict, Optional, Type

from requests import request

from pydrag import utils
from pydrag.exceptions import ApiError
from pydrag.models.common import BaseModel, Config, ListModel

config = Config.instance()


class ApiMixin:
    @classmethod
    def get_session(cls):
        if not config.session:
            from pydrag.models.auth import AuthSession

            config.session = AuthSession.get()
        return config.session

    @classmethod
    def retrieve(
        cls,
        bind: Type[BaseModel],
        many: Optional[str] = None,
        params: Dict = dict(),
    ):
        return cls._perform(
            method="GET",
            bind=bind,
            many=many,
            params=params,
            stateful=False,
            authenticate=False,
        )

    @classmethod
    def submit(
        cls,
        bind: Type[BaseModel],
        many: Optional[str] = None,
        params: Dict = dict(),
        stateful: bool = False,
        authenticate: bool = False,
    ):
        return cls._perform(
            method="POST",
            bind=bind,
            many=many,
            params=params,
            stateful=stateful,
            authenticate=authenticate,
        )

    @classmethod
    def _perform(
        cls,
        method: str,
        bind: Type[BaseModel],
        many: Optional[str],
        params: Dict,
        stateful: bool,
        authenticate: bool,
    ):
        data: Dict = dict()
        query: Dict = dict()
        if method == "GET":
            query = cls.prepare_params(params, stateful, authenticate)
        else:
            data = cls.prepare_params(params, stateful, authenticate)

        response = request(
            method=method, url=config.api_url, data=data, params=query
        )
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        cls.raise_for_error(body)
        obj = cls.bind_data(bind, body, many)
        obj.params = params
        return obj

    @classmethod
    def prepare_params(
        cls, params: Dict, stateful=False, authenticate=False
    ) -> dict:

        params = dict(
            (k, str(int(v is True) if type(v) == bool else v))
            for k, v in params.items()
            if v is not None
        )
        params.update(dict(format="json", api_key=config.api_key))

        if authenticate:
            params.update(
                dict(username=config.username, authToken=config.auth_token)
            )

        if stateful:
            params.update(dict(sk=cls.get_session().key))

        if authenticate or stateful:
            params.update(dict(api_sig=cls.sign(params)))

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
    def raise_for_error(body: Dict):
        if "error" in body:
            raise ApiError(**body)

    @staticmethod
    def sign(params):
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [str(k) + str(params[k]) for k in keys if params.get(k)]
        signature.append(str(config.api_secret))
        return utils.md5("".join(signature))


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
        "albumArtist": "album_artist",
        "streamId": "stream_id",
        "albumArtist": "album_artist",
        "realname": "real_name",
        "recenttrack": "recent_track",
        "ontour": "on_tour",
        "num_res": "limit",
        "title": "name",
    }

    """
    A list of fields that dont make make sense in the api responses
    Either they don't always have the same value type or have a dev message
    """
    fixme = [
        "subscriber",
        "type",
        "scrobblesource",
        "bootstrap",
        "streamable",
        "ignoredMessage",
    ]

    return {map.get(k, k): v for k, v in data if k not in fixme}
