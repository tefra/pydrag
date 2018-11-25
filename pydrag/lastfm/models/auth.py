from typing import TypeVar

from attr import dataclass

from pydrag.core import BaseModel

V = TypeVar("V", bound="AuthSession")


@dataclass
class AuthSession(BaseModel):
    key: str
    name: str
    subscriber: int

    @classmethod
    def get(cls) -> V:
        """
        Create a web service session for a user.

        :returns: AuthSession
        """
        return cls.submit(
            authenticate=True, params=dict(method="auth.getMobileSession")
        )
