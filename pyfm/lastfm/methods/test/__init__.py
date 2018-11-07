import os
from unittest import TestCase

from vcr import config, VCR

where_am_i = os.path.dirname(os.path.realpath(__file__))

fixture = config.VCR(
    filter_query_parameters=["api_key"],
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
