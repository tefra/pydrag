from typing import Dict, Optional, Type

from requests import request

from pydrag import utils
from pydrag.exceptions import ApiError
from pydrag.models.common import BaseModel, Config, ListModel
from pydrag.utils import get_nested


class ApiMixin:
    @classmethod
    def get_session(cls) -> "AuthSession":  # type: ignore
        """
        Return the session from configuration or attempt to authenticate the
        configuration user.

        :rtype: :class:`~pydrag.models.auth.AuthSession`
        """
        cfg = Config.instance()
        if not cfg.session:
            from pydrag.models.auth import AuthSession

            cfg.session = AuthSession.authenticate()
        return cfg.session

    @classmethod
    def retrieve(
        cls,
        bind: Type[BaseModel],
        flatten: Optional[str] = None,
        params: Optional[Dict] = None,
    ):
        """
        Perform an api retrieve/get resource action.

        :param bind: Class type to construct from the api response.
        :type bind: :class:`~pydrag.models.common.BaseModel`
        :param str flatten: A dot separated string used to flatten nested list of values
        :param Dict params: A dictionary of query string params
        :rtype: :class:`~pydrag.models.common.BaseModel`
        """
        return cls._perform(
            method="GET",
            bind=bind,
            flatten=flatten,
            params=params or {},
            sign=False,
            stateful=False,
            authenticate=False,
        )

    @classmethod
    def submit(
        cls,
        bind: Type[BaseModel],
        flatten: Optional[str] = None,
        params: Optional[Dict] = None,
        sign: bool = False,
        stateful: bool = False,
        authenticate: bool = False,
    ):
        """
        Perform an api write/update resource action.

        :param bind: Class type to construct from the api response.
        :type bind: :class:`~pydrag.models.common.BaseModel`
        :param str flatten: A dot separated string used to flatten nested list of values
        :param Dict params: A dictionary of body params
        :param bool sign: Sign the request with the api secret
        :param bool stateful: Requires a session
        :param bool authenticate: Perform an authentication request
        :rtype: :class:`~pydrag.models.common.BaseModel`
        """
        return cls._perform(
            method="POST",
            bind=bind,
            flatten=flatten,
            params=params or {},
            sign=sign,
            stateful=stateful,
            authenticate=authenticate,
        )

    @classmethod
    def _perform(
        cls,
        method: str,
        bind: Type[BaseModel],
        flatten: Optional[str],
        params: Dict,
        sign: bool,
        stateful: bool,
        authenticate: bool,
    ):
        """
        Orchestrate the request, error handling and response deserialization.

        :param str method: Http method POST/GET
        :param bind: Class type to construct from the api response.
        :type bind: :class:`~pydrag.models.common.BaseModel`
        :param str flatten: A dot separated string used to flatten nested
        :param Dict params: A dictionary of body or query string params
        :param bool sign: Sign the request with the api secret
        :param bool stateful: Requires a session
        :param bool authenticate: Perform an authentication request
        :rtype: :class:`~pydrag.models.common.BaseModel`
        """
        data: Dict = dict()
        query: Dict = dict()
        if method == "GET":
            query = cls.prepare_params(params, sign, stateful, authenticate)
        else:
            data = cls.prepare_params(params, sign, stateful, authenticate)

        cfg = Config.instance()
        response = request(
            method=method, url=cfg.api_url, data=data, params=query
        )
        response.raise_for_status()
        body = response.json(object_pairs_hook=pythonic_variables)
        cls.raise_for_error(body)
        obj = cls.bind_data(bind, body, flatten)
        obj.params = params
        return obj

    @classmethod
    def prepare_params(
        cls, params: Dict, sign: bool, stateful: bool, authenticate: bool
    ) -> dict:
        """
        Perform common parameter tasks before sending the web request.

        * Filter out None values,
        * Set the preferred api format ``json``
        * Add the api key, session or signature based on the state flags

        :param Dict params: A dictionary of body or query string params
        :param bool sign: Sign the request with the api secret
        :param bool stateful: Add the session key to the params
        :param bool authenticate: Add the username and auth token to the params
        :rtype: Dict
        """
        cfg = Config.instance()
        params = dict(
            (k, str(int(v is True) if isinstance(v, bool) else v))
            for k, v in params.items()
            if v is not None
        )
        params.update(dict(format="json", api_key=cfg.api_key))

        if authenticate:
            params.update(
                dict(username=cfg.username, authToken=cfg.auth_token)
            )

        if stateful:
            params.update(dict(sk=cls.get_session().key))

        if authenticate or stateful or sign:
            params.update(dict(api_sig=cls.sign(params)))

        return params

    @classmethod
    def bind_data(
        cls,
        bind: Type[BaseModel],
        body: Optional[Dict],
        flatten: Optional[str] = None,
    ):
        """
        Construct a BaseModel from the response body and the flatten directive.

        :param bind: Class type to construct from the api response.
        :type bind: :class:`~pydrag.models.common.BaseModel`
        :param Dict body: The api response
        :param str flatten: A dot separated string used to flatten nested list of values
        :rtype: :class:`~pydrag.models.common.BaseModel`
        """
        if not body:
            return bind()

        data = body[next(iter(body.keys()))]
        if data and not isinstance(data, Dict):
            data = body

        if flatten is None:
            return bind.from_dict(data)

        keys = flatten.split(".")
        items = get_nested(data, keys, ensure_list=True)
        data.pop(next(iter(keys)))
        data.update(dict(data=[bind.from_dict(i) for i in items]))
        return ListModel.from_dict(data)

    @staticmethod
    def raise_for_error(body: Dict):
        """
        Parse and raise api errors.

        :param Dict body: Response body
        :raise: :class:`~pydrag.exceptions.ApiError`
        """
        if "error" in body:
            raise ApiError(**body)

    @staticmethod
    def sign(params: Dict) -> str:
        """
        Last.fm signing formula for webservice calls. Exclude format, sort
        params, append the api secret key and hash the params string.

        :param Dict params:
        :rtype: str
        """
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [str(k) + str(params[k]) for k in keys if params.get(k)]
        signature.append(str(Config.instance().api_secret))
        return utils.md5("".join(signature))  # type: ignore


def pythonic_variables(data):
    map = {
        "albummatches": "albums",
        "artistmatches": "artists",
        "trackmatches": "tracks",
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
        "opensearch:totalResults": "total",
        "toptags": "top_tags",
        "streamId": "stream_id",
        "albumArtist": "album_artist",
        "realname": "real_name",
        "recenttrack": "recent_track",
        "ontour": "on_tour",
        "num_res": "limit",
        "title": "name",
        "userloved": "loved",
        "opensearch:Query": "query",
        "perPage": "limit",
        "position": "rank",
    }

    # A list of fields that dont make make sense in the api responses
    # Either they don't always have the same value type or have a dev message
    fixme = [
        "subscriber",
        "type",
        "scrobblesource",
        "bootstrap",
        "streamable",
        "ignoredMessage",
        "totalPages",  # I can do the math
        "opensearch:startIndex",  # I can do the math,
        "ignored",
        "accepted",
        "role",
    ]

    return {map.get(k, k): v for k, v in data if k not in fixme}
