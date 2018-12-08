from attr import dataclass

from pydrag.models.common import BaseModel
from pydrag.services import ApiMixin


@dataclass
class AuthSession(BaseModel, ApiMixin):
    key: str
    name: str

    @classmethod
    def get(cls) -> "AuthSession":
        """
        Create a web service session for a user.

        :rtype: :class:`~pydrag.models.auth.AuthSession`
        """
        return cls.submit(
            bind=AuthSession,
            authenticate=True,
            params=dict(method="auth.getMobileSession"),
        )
