from pyfm.lastfm import api
from pyfm.lastfm.models import UserFriends


class Library:
    """
    Last.fm Library API interface for easy access/navigation
    """

    def __init__(self, user: str):
        """
        user (Required) : The last.fm username to make api calls
        :param str user:
        """
        self.user = user

    @api.operation
    def get_artists(self, limit: int = 50, page: int = 1) -> UserFriends:
        """
        :param page: The page number to fetch. Defaults to first page.
        :param limit: The number of results to fetch per page. Defaults to 50.
        :returns: LibraryArtists
        """
        return dict(user=self.user, page=page, limit=limit)
