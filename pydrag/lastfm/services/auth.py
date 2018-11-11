from pydrag.lastfm import api
from pydrag.lastfm.api import POST
from pydrag.lastfm.models.auth import AuthMobileSession, AuthSession, AuthToken


class AuthService:
    @api.operation(signed=False)
    def get_token(self) -> AuthToken:
        """
        Fetch an unathorized request token for an API account. Open the
        AuthToken.auth_url where the user must authorize the token use the
        get_session with the same authorized token to retrieve the use session.

        :returns: AuthToken
        """
        return None

    @api.operation(method=POST, signed=True)
    def get_session(self, token: str) -> AuthSession:
        return dict(token=token)

    @api.operation(method=POST, signed=True, auth=True)
    def get_mobile_session(self) -> AuthMobileSession:
        """
        Create a web service session for a user. Used for authenticating a user
        when the password can be inputted by the user. Accepts email address as
        well, so please use the username supplied in the output.

        :returns: AuthMobileSession
        """
        return None
