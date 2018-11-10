import os
from unittest import TestCase
import re
from vcr import config, VCR

where_am_i = os.path.dirname(os.path.realpath(__file__))

censored_parameters = [
    ("token", "USER_TOKEN"),
    ("sk", "USER_SESSION"),
    ("api_sig", "API_SIG"),
    ("api_key", "LAST_FM_API_KEY"),
    ("authToken", "USER_AUTH_TOKEN"),
]


def censore_response(response):
    body = response["body"]["string"]
    body = re.sub(b"[A-Za-z0-9-_]{32}", b"CENSORED", body)
    response["body"]["string"] = body
    return response


fixture = config.VCR(
    filter_query_parameters=censored_parameters,
    filter_post_data_parameters=censored_parameters,
    before_record_response=censore_response,
    cassette_library_dir=os.path.join(where_am_i, "fixtures"),
    path_transformer=VCR.ensure_suffix(".json"),
    serializer="json",
)


def s(value):
    if type(value) == int:
        return str(value)

    if isinstance(value, list):
        for idx, v in enumerate(value):
            value[idx] = s(v)

    elif isinstance(value, dict):
        if "streamable" in value:
            del value["streamable"]

        for k, v in value.items():
            value[k] = s(v)
    return value


class MethodTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        super(MethodTestCase, self).setUp()

    def assertDictEqual(self, d1, d2, msg=None):
        super(MethodTestCase, self).assertDictEqual(s(d1), s(d2))
