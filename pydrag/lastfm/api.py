import hashlib
import inspect
from functools import partial, wraps
from typing import Union
from urllib.parse import urlencode

import requests
from requests import Response

from pydrag.lastfm import GET, POST, config, md5


def operation(
    func=None, *, method=GET, signed=False, auth=False, stateful=False
):
    if func is None:
        return partial(
            operation,
            method=method,
            signed=signed,
            auth=auth,
            stateful=stateful,
        )

    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        func(obj, *args, **kwargs) or dict()
        return Request(
            namespace=obj.__class__.__name__.replace("Service", ""),
            method=func.__name__,
            http_method=method,
            clazzz=inspect.signature(func).return_annotation,
            signed=signed,
            auth=auth,
            stateful=stateful,
            params=func(obj, *args, **kwargs) or dict(),
        ).perform()

    return wrapper


class Request:
    def __init__(
        self,
        namespace: str,
        method: str,
        clazzz: object,
        http_method: str,
        signed: bool,
        auth: bool,
        stateful: bool,
        params: dict,
    ):
        self.namespace = namespace
        self.method = method
        self.clazzz = clazzz
        self.http_method = http_method
        self.signed = signed
        self.auth = auth
        self.stateful = stateful
        self.params = dict((k, v) for k, v in params.items() if v is not None)

        if stateful and "sk" not in params:
            from pydrag.lastfm.services.auth import AuthService

            self.params["sk"] = AuthService().get_mobile_session().key

    def get_request_params(self):
        res = self.params.copy()
        comp = self.method.split("_")
        method = comp[0] + "".join(x.title() for x in comp[1:])

        res.update(
            dict(
                method="{}.{}".format(self.namespace.lower(), method),
                format="json",
                api_key=config.api_key,
            )
        )

        for key in res.keys():
            _type = type(res[key])
            if _type == bool:
                res[key] = int(res[key] is True)
            else:
                res[key] = str(res[key])
        return res

    def perform(self):
        url = config.api_root_url
        params = self.get_request_params()

        if self.auth:
            params.update(
                dict(
                    username=config.username,
                    authToken=md5(str(config.username) + str(config.password)),
                )
            )

        # TODO somehow signed disappears on stateful signed requests
        if self.signed or "sk" in self.params:
            params["api_sig"] = self.sign(params)

        if self.http_method == GET:
            url += "?{}".format(urlencode(params))
            response = requests.get(url)
        elif self.http_method == POST:
            response = requests.post(url, data=params)

        response.raise_for_status()
        body = response.json()
        return self.bind(response, body)

    def bind(self, resp: Response, body: Union[dict, list, None]):
        assert isinstance(body, dict)

        if body:
            data = body.get(next(iter(body.keys())))
            if isinstance(data, dict):
                obj = self.clazzz.from_dict(data)
            else:
                obj = self.clazzz(data)
        else:
            obj = self.clazzz()

        obj.response = resp
        obj.namespace = self.namespace
        obj.method = self.method
        obj.params = self.params
        obj.signed = self.signed
        obj.auth = self.auth
        obj.stateful = self.stateful
        obj.http_method = self.http_method
        return obj

    @staticmethod
    def sign(params):
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [str(k) + str(params[k]) for k in keys if params.get(k)]
        signature.append(str(config.api_secret))
        return hashlib.md5("".join(signature).encode("utf-8")).hexdigest()
