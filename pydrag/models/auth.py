from attr import dataclass

from pydrag.models.common import BaseModel
from pydrag.models.common import Config
from pydrag.services import ApiMixin


@dataclass
class AuthSession(BaseModel, ApiMixin):
    """
    Last.FM authentication api wrapper.

    :param key: Session key
    :param name: Authenticated user
    """

    key: str
    name: str

    @classmethod
    def authenticate(cls) -> "AuthSession":
        """
        Create a web service session for a user.  Session keys have an infinite
        lifetime by default. You are recommended to store the key securely.
        Users are able to revoke privileges for your application on their
        Last.fm settings screen, rendering session keys invalid.

        :rtype: :class:`~pydrag.models.auth.AuthSession`
        """
        return cls.submit(
            bind=AuthSession,
            authenticate=True,
            params={"method": "auth.getMobileSession"},
        )

    @classmethod
    def from_token(cls, token: str) -> "AuthSession":
        """
        After authorizing a token use this method to retrieve a session.
        Session keys have an infinite lifetime by default. You are recommended
        to store the key securely. Users are able to revoke privileges for your
        application on their Last.fm settings screen, rendering session keys
        invalid.

        :rtype: :class:`~pydrag.models.auth.AuthSession`
        """
        return cls.submit(
            bind=AuthSession,
            sign=True,
            params={"token": token, "method": "auth.getSession"},
        )


@dataclass
class AuthToken(BaseModel, ApiMixin):
    """
    Last.FM authorization token api wrapper.

    :param token: Authorization token
    """

    token: str

    @property
    def auth_url(self):
        return Config.auth_url.format(self.token, Config.instance().api_key)

    @classmethod
    def generate(cls) -> "AuthToken":
        """
        Fetch an unauthorized request token for an API account. The user must
        follow the the auth_link and grant access to the token. Afterwards we
        retrieve a session for the authorized token. Tokens have 60 minutes
        time to live.

        :rtype: :class:`~pydrag.models.auth.AuthToken`
        """

        return cls.retrieve(bind=AuthToken, params={"method": "auth.getToken"})
