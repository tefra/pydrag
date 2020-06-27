import json
import os
import re
from unittest import TestCase

import vcr

from pydrag.models.common import Config

try:
    config = Config.instance()
except ValueError:
    Config.instance(api_key="key")

where_am_i = os.path.dirname(os.path.realpath(__file__))
fixtures_dir = os.path.join(where_am_i, "models", "fixtures")

censored_parameters = [
    ("token", "USER_TOKEN"),
    ("sk", "USER_SESSION"),
    ("api_sig", "API_SIG"),
    ("api_key", "LAST_FM_API_KEY"),
    ("authToken", "USER_AUTH_TOKEN"),
]


def censor_response(response):
    body = response["body"]["string"]
    body = re.sub(b"[A-Za-z0-9-_]{32}", b"CENSORED", body)
    response["body"]["string"] = body
    return response


fixture = vcr.config.VCR(
    filter_query_parameters=censored_parameters,
    filter_post_data_parameters=censored_parameters,
    before_record_response=censor_response,
    cassette_library_dir=fixtures_dir,
    path_transformer=vcr.VCR.ensure_suffix(".json"),
    serializer="json",
)


class MethodTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        Config.instance().session = None
        super().setUp()

    @staticmethod
    def load_fixture(file_name):
        path = f"{fixtures_dir}/{file_name}_expected.json"
        try:
            with open(path) as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def assertFixtureEqual(self, file_name, actual):
        expected = self.load_fixture(file_name)
        if expected is None:
            path = f"{fixtures_dir}/{file_name}_expected.json"
            with open(path, "w") as f:
                json.dump(actual, f, indent=4, sort_keys=True)
                f.write("\n")
            return self.assertFixtureEqual(file_name, actual)

        self.assertDictEqual(expected, actual)
