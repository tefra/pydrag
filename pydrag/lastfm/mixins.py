from pydrag.lastfm.api import Request


class PagerMixin:
    """
    Pagination mixin to navigate through lists.

    If has next or has prev return true inc/dec the page parameter and
    make the exact same request that produced the current object. It's
    important that we copy all the original request parameters from one
    instance to the next.
    """

    def get_page(self):
        return getattr(self.attr, "page")

    def get_limit(self):
        return getattr(self.attr, "limit")

    def get_total(self):
        return getattr(self.attr, "total")

    def get_total_pages(self):
        return getattr(self.attr, "total_pages")

    def get_next(self):
        if not self.has_next():
            raise StopIteration()

        params = self.params.copy()
        params["page"] += 1
        return self._request(params)

    def get_prev(self):
        if not self.has_prev():
            raise StopIteration()

        params = self.params.copy()
        params["page"] -= 1
        return self._request(params)

    def has_next(self):
        page = self.get_page()
        return bool(page and page < self.get_total_pages())

    def has_prev(self):
        page = self.get_page()
        return bool(page and page > 1)

    def _request(self, params):
        return Request(
            namespace=self.namespace,
            method=self.method,
            clazzz=self.__class__,
            http_method=self.http_method,
            signed=self.signed,
            auth=self.auth,
            stateful=self.stateful,
            params=params,
        ).perform()
