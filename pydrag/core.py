from collections import UserList
from typing import Dict, List, Optional, Sequence, Type, TypeVar
from urllib.parse import urlencode

import attr
import requests

from pydrag import config
from pydrag.utils import md5

T = TypeVar("T")


class BaseModel:
    params: Optional[dict] = attr.attrib(init=False)

    def to_dict(self: "BaseModel") -> Dict:
        """
        Convert our object to a traditional dictionary. Filter out None values
        and dictionary values. The last one is like a validation for the unit
        tests in case we forgot to properly deserialize an dict to an object.

        :rtype: Dict
        """
        return attr.asdict(
            self, filter=lambda f, v: v is not None and type(v) != dict
        )

    @classmethod
    def from_dict(cls: Type, data: dict) -> "BaseModel":
        for f in attr.fields(cls):
            if f.name not in data or data[f.name] is None:
                continue

            if f.type == str or f.type == Optional[str]:
                data[f.name] = str(data[f.name])
            elif f.type == int or f.type == Optional[int]:
                data[f.name] = int(data[f.name])
            elif f.type == float or f.type == Optional[float]:
                data[f.name] = float(data[f.name])

        return cls(**data)


@attr.dataclass(cmp=False)
class ListModel(UserList, Sequence[T], extra=list):
    data: List[T] = []

    def to_dict(self) -> Dict:
        return dict(data=[item.to_dict() for item in self])


@attr.dataclass
class RawResponse(BaseModel):
    data: Optional[dict] = None

    def to_dict(self):
        return self.data

    @classmethod
    def from_dict(cls, data):
        return cls(data)


class ApiMixin:
    @classmethod
    def validate(cls, bind, params):
        assert "method" in params
        if bind is None:
            bind = RawResponse
        return bind, cls.prepare_params(params)

    @classmethod
    def retrieve(cls, bind=None, many=None, params={}):
        bind, data = cls.validate(bind, params)
        url = "{}?{}".format(config.api_root_url, urlencode(data))
        response = requests.get(url)
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        obj = cls.bind_data(bind, body, many)
        obj.params = params
        return obj

    @classmethod
    def submit(
        cls,
        bind=None,
        many=None,
        stateful=False,
        authenticate=False,
        params={},
    ):
        bind, data = cls.validate(bind, params)
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
        assert isinstance(body, dict)

        if not body:
            return bind()

        data = body[next(iter(body.keys()))]
        if many is None:
            return bind.from_dict(data)

        try:
            for m in many.split("."):
                data = data.pop(m)

            if isinstance(data, dict):
                data = [data]

            items: list = [bind.from_dict(d) for d in data]
        except KeyError:
            items = []

        return ListModel(data=items)

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
