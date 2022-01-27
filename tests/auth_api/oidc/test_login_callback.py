from datetime import datetime
import pytest

from typing import Dict, Any
from unittest.mock import MagicMock
from flask.testing import FlaskClient

from origin.tokens import TokenEncoder
from origin.api.testing import (
    assert_base_url,
    assert_query_parameter,
)

from auth_api.db import db
from auth_api.endpoints import AuthState
from auth_api.config import (
    OIDC_LOGIN_CALLBACK_PATH,
    TERMS_URL,
    TERMS_ACCEPT_URL,
)


class TestOidcLoginCallbackSubjectUnknown:
    """
    Tests cases where returning to login callback, and the Identity
    Provider's subject is unknown to the system.
    """

    @pytest.mark.integrationtest
    def test__user_does_not_exist__should_redirect_to_terms(
        self,
        client: FlaskClient,
        mock_session: db.Session,
        mock_get_jwk: MagicMock,
        mock_fetch_token: MagicMock,
        state_encoder: TokenEncoder[AuthState],
        jwk_public: str,
        ip_token: Dict[str, Any],
        token_issued: datetime,
        token_expires: datetime,
        token_tin: str,
    ):
        """
        When logging in, if the user doesn't exist the user needs
        to be redirected to the terms and conditions so they can
        accept or decline them
        """

        # -- Arrange ----------------------------------------------------------

        state = AuthState(
            fe_url='http://foobar.com',
            return_url='http://redirect-here.com/foobar',
            issued=token_issued,
            expires=token_expires,
            tin=token_tin,
            id_token=ip_token['id_token'],
        )

        state_encoded = state_encoder.encode(state)
        mock_get_jwk.return_value = jwk_public
        mock_fetch_token.return_value = ip_token

        # -- Act --------------------------------------------------------------

        r = client.get(
            path=OIDC_LOGIN_CALLBACK_PATH,
            query_string={'state': state_encoded},
        )

        # -- Assert -----------------------------------------------------------

        redirect_location = r.headers['Location']

        assert r.status_code == 307

        # Redirect to terms should be to correct URL (without
        # taking query parameters into consideration)
        assert_base_url(
            url=redirect_location,
            expected_base_url='http://foobar.com/terms',
            check_path=True,
        )

        # Redirect to terms must have correct query params

        assert_query_parameter(
            url=redirect_location,
            name='terms_url',
            value=TERMS_URL,
        )

        assert_query_parameter(
            url=redirect_location,
            name='terms_accept_url',
            value=TERMS_ACCEPT_URL,
        )

        assert_query_parameter(
            url=redirect_location,
            name='state',
            value=state_encoded,
        )
