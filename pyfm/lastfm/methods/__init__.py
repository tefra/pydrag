from typing import Optional
from urllib.parse import urlencode

import requests

from pyfm.lastfm import api_key, api_root_url
from pyfm.lastfm import models

Page = Optional[int]
Limit = Optional[int]
Date = Optional[str]


def get(namespace: str, method: str, params: dict, data=None):
    prep_params = params.copy()
    prep_params.update(
        dict(
            method="{}.{}".format(namespace.lower(), method.replace("_", "")),
            format="json",
            api_key=api_key,
        )
    )

    for key in params.keys():
        if type(params.get(key)) == bool:
            params[key] = int(params[key] is True)

    url = "{}?{}".format(api_root_url, urlencode(prep_params))
    response = requests.get(url)
    response.raise_for_status()
    body = response.json()
    if isinstance(body, dict):
        model_class = method.replace("_", " ").replace("get", "").title()
        model_class = "".join(x for x in model_class if not x.isspace())

        if not model_class.startswith(namespace.title()):
            model_class = "{}{}".format(namespace.title(), model_class)

        root = body.get(next(iter(body.keys())))
        klass = getattr(models, model_class)
        obj = klass.from_dict(root)
        obj.response = response
        obj.namespace = namespace
        obj.method = method
        obj.params = params
        obj.data = data
        return obj


def apimethod(func):
    def func_wrapper(self, *args, **kwargs):
        method = func.__name__
        namespace = self.__class__.__name__

        params = {}
        data = None
        result = func(self, *args, **kwargs)
        if isinstance(result, tuple):
            params, data = result
        elif isinstance(result, dict):
            params = result
            data = None

        params = dict((k, v) for k, v in params.items() if v is not None)

        return get(
            namespace=namespace, method=method, params=params, data=data
        )

    return func_wrapper
