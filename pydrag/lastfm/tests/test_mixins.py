from unittest import TestCase, mock

from pydrag.lastfm.api import Request
from pydrag.lastfm.models.common import Attributes, AttrModel


class PaginatedModel(AttrModel):
    pass


class PagerMixinTests(TestCase):
    def setUp(self):
        self.obj = PaginatedModel(attr=Attributes())
        super(PagerMixinTests, self).setUp()

    def test_get_page(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertIsNone(self.obj.get_page())

        self.obj.attr.page = 1
        self.assertEqual(1, self.obj.get_page())

    def test_get_limit(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertIsNone(self.obj.get_limit())

        self.obj.attr.limit = 1
        self.assertEqual(1, self.obj.get_limit())

    def test_get_total_pages(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertIsNone(self.obj.get_total_pages())

        self.obj.attr.total_pages = 1
        self.assertEqual(1, self.obj.get_total_pages())

    def test_get_total(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertIsNone(self.obj.get_total())

        self.obj.attr.total = 1
        self.assertEqual(1, self.obj.get_total())

    def test_has_prev(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertFalse(self.obj.has_prev())

        self.obj.attr.page = 1
        self.assertFalse(self.obj.has_prev())

        self.obj.attr.page = 2
        self.assertTrue(self.obj.has_prev())

    def test_has_next(self):
        self.obj = PaginatedModel(attr=Attributes())
        self.assertFalse(self.obj.has_next())

        self.obj.attr.page = 1
        self.obj.attr.total_pages = 1
        self.assertFalse(self.obj.has_next())

        self.obj.attr.total_pages = 2
        self.assertTrue(self.obj.has_next())

    @mock.patch.object(PaginatedModel, "_request")
    def test_get_prev(self, mock_request):
        self.obj = PaginatedModel(attr=Attributes())

        with self.assertRaises(StopIteration):
            self.obj.get_prev()

        mock_request.return_value = "foo"
        self.obj.attr.page = 2
        self.obj.params = dict(page=2)
        actual = self.obj.get_prev()

        self.assertEqual("foo", actual)
        mock_request.assert_called_once_with(dict(page=1))

    @mock.patch.object(PaginatedModel, "_request")
    def test_get_next(self, mock_request):
        with self.assertRaises(StopIteration):
            self.obj.get_next()

        mock_request.return_value = "foo"
        self.obj.attr.page = 2
        self.obj.attr.total_pages = 3
        self.obj.params = dict(page=2)
        actual = self.obj.get_next()

        self.assertEqual("foo", actual)
        mock_request.assert_called_once_with(dict(page=3))

    @mock.patch.object(Request, "perform", return_value="performed")
    @mock.patch.object(Request, "__init__", return_value=None)
    def test__request(self, mock_init, mock_perform):
        self.obj.namespace = "namespace"
        self.obj.method = "method"
        self.obj.http_method = "put"
        self.obj.signed = "signed"
        self.obj.auth = "auth"
        self.obj.stateful = "stateful"

        actual = self.obj._request(dict(foo="bar"))
        self.assertEqual("performed", actual)

        mock_init.assert_called_once_with(
            namespace="namespace",
            method="method",
            clazzz=PaginatedModel,
            http_method="put",
            signed="signed",
            auth="auth",
            stateful="stateful",
            params=dict(foo="bar"),
        )
