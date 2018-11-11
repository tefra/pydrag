from pydrag.core import BaseModel
from pydrag.lastfm.api import Request


class PaginatedModel(BaseModel):
    @property
    def page(self):
        return getattr(self.attr, "page")

    @property
    def limit(self):
        return getattr(self.attr, "perPage")

    @property
    def total(self):
        return getattr(self.attr, "total")

    @property
    def total_pages(self):
        return getattr(self.attr, "totalPages")

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
        return self.page and self.page < self.total_pages

    def has_prev(self):
        return self.page and self.page > 1

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
