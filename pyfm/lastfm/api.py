import hashlib
from functools import partial, wraps
from urllib.parse import urlencode

import requests

from lastfm import md5
from pyfm import BaseModel
from pyfm.lastfm import config, models, GET, POST


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
        return Request(
            namespace=obj.__class__.__name__,
            method=func.__name__,
            http_method=method,
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
        http_method: str,
        signed: bool,
        auth: bool,
        stateful: bool,
        params: dict,
    ):
        self.namespace = namespace
        self.method = method
        self.http_method = http_method
        self.signed = signed
        self.auth = auth
        self.stateful = stateful
        self.params = dict((k, v) for k, v in params.items() if v is not None)

        if stateful and "sk" not in params:
            from lastfm.methods import Auth

            self.params["sk"] = Auth().get_mobile_session().key

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
            if type(res.get(key)) == bool:
                res[key] = int(res[key] is True)
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

        if self.signed:
            params["api_sig"] = self.sign(params)

        if self.http_method == GET:
            url += "?{}".format(urlencode(params))
            response = requests.get(url)
        elif self.http_method == POST:
            response = requests.post(url, data=params)

        response.raise_for_status()
        body = response.json()
        return self.bind(response, body)

    def bind(self, response, body):
        assert isinstance(body, dict)

        if not body:
            obj = BaseModel()
        else:
            klass = self.get_klass()
            data = body.get(next(iter(body.keys())))
            if isinstance(data, dict):
                obj = klass.from_dict(data)
            else:
                obj = klass(data)

        obj.response = response
        obj.namespace = self.namespace
        obj.method = self.method
        obj.params = self.params
        return obj

    def get_klass(self):
        replace = (("_", " "), ("add", ""), ("get", ""))
        model_class = self.method
        for s, r in replace:
            model_class = model_class.replace(s, r)

        model_class = "".join(
            x for x in model_class.title() if not x.isspace()
        )
        if not model_class.startswith(self.namespace.title()):
            model_class = "{}{}".format(self.namespace.title(), model_class)
        return getattr(models, model_class)

    def sign(self, params):
        keys = sorted(params.keys())
        keys.remove("format")

        signature = [k + params[k] for k in keys if params.get(k)]
        signature.append(str(config.api_secret))
        bytes = "".join(signature).encode("utf-8")
        return hashlib.md5(bytes).hexdigest()
