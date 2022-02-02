"""
conftest.py according to pytest docs:
https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re#conftest-py-plugins
"""
import pytest
from unittest.mock import patch
from testcontainers.postgres import PostgresContainer

from origin.sql import POSTGRES_VERSION, SqlEngine
from auth_api.db import db as _db

# # -- SQL --------------------------------------------------------------------

class TestQueryBase:
    @pytest.fixture(scope='function')
    def psql_uri(self):
        """
        TODO
        """
        image = f'postgres:{POSTGRES_VERSION}'

        with PostgresContainer(image) as psql:
            yield psql.get_connection_url()

    @pytest.fixture(scope='function')
    def db(self, psql_uri: str) -> SqlEngine:
        """
        TODO
        """
        with patch('auth_api.db.db.uri', new=psql_uri):
            yield _db

    @pytest.fixture(scope='function')
    def seeded_session(self, db: SqlEngine) -> SqlEngine.Session:
        """
        TODO
        """
        db.apply_schema()

        with db.make_session() as session:
            yield session
