from unittest import TestCase

from pydrag.core import RawResponse


class RawResponseTests(TestCase):
    def test_to_dict(self):
        raw = RawResponse.from_dict(dict(a=1))
        self.assertEqual(dict(a=1), raw.to_dict())

    def test_from_dict(self):
        raw = RawResponse.from_dict(dict(a=1))
        self.assertEqual(dict(a=1), raw.data)
