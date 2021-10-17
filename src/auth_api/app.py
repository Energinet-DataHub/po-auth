from energytt_platform.api import Application

from .config import (
    INTERNAL_TOKEN_SECRET,
    OIDC_LOGIN_CALLBACK_PATH,
    OIDC_LOGIN_CALLBACK_URL,
    OIDC_SSN_VALIDATE_CALLBACK_PATH,
    OIDC_SSN_VALIDATE_CALLBACK_URL,
    OIDC_LOGOUT_CALLBACK_PATH,
)
from .endpoints import (
    ForwardAuth,
    InspectToken,
    CreateTestToken,
    OpenIdLogin,
    OpenIDLoginCallback,
    OpenIDSsnCallback,
    OpenIdLogout,
    OpenIdLogoutRedirect,
    OpenIdLogoutCallback,
)


def create_app() -> Application:
    """
    Creates a new instance of the application.
    """

    app = Application.create(
        name='Auth API',
        secret=INTERNAL_TOKEN_SECRET,
        health_check_path='/health',
    )

    # -- OpenID Connect Login ------------------------------------------------

    # Login
    app.add_endpoint(
        method='GET',
        path='/oidc/login',
        endpoint=OpenIdLogin(),
    )

    # Callback, after logging in
    app.add_endpoint(
        method='GET',
        path=OIDC_LOGIN_CALLBACK_PATH,
        endpoint=OpenIDLoginCallback(url=OIDC_LOGIN_CALLBACK_URL),
    )

    # Callback, after verifying SSN
    app.add_endpoint(
        method='GET',
        path=OIDC_SSN_VALIDATE_CALLBACK_PATH,
        endpoint=OpenIDSsnCallback(url=OIDC_SSN_VALIDATE_CALLBACK_URL),
    )

    # -- OpenID Connect Logout -----------------------------------------------

    app.add_endpoint(
        method='GET',
        path='/oidc/logout',
        endpoint=OpenIdLogout(),
    )

    app.add_endpoint(
        method='GET',
        path='/oidc/logout/redirect',
        endpoint=OpenIdLogoutRedirect(),
    )

    app.add_endpoint(
        method='GET',
        path=OIDC_LOGOUT_CALLBACK_PATH,
        endpoint=OpenIdLogoutCallback(),
    )

    # -- Træfik integration --------------------------------------------------

    app.add_endpoint(
        method='GET',
        path='/token/forward-auth',
        endpoint=ForwardAuth(),
    )

    # -- Testing/misc --------------------------------------------------------

    app.add_endpoint(
        method='GET',
        path='/token/inspect',
        endpoint=InspectToken(),
    )

    app.add_endpoint(
        method='POST',
        path='/token/create-test-token',
        endpoint=CreateTestToken(),
    )

    return app
