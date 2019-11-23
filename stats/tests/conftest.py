import json
import pytest
from flask import jsonify
import flask_jwt_extended as jwt

from stats.app import create_app
from stats.extensions import db
from stats.api import search


@pytest.fixture
def app():
    app = create_app(config='stats/tests/config_test.py', blueprints=search)

    return app


@pytest.fixture
def client_factory(app):

    class ClientFactory:

        def __init__(self, app):
            self._app = app

        def get(self):
            return self._app.test_client()

    return ClientFactory(app)

def _init_database(db):
    '''
    Initializes the database for testing.
    It will be overwritten in the test file
    '''
    pass

@pytest.fixture
def client(app, client_factory):
    return client_factory.get()

@pytest.fixture
def database(app):
    '''
    Provides a reference to the temporary database in the app context. Use
    this instance instead of importing db from monolith.db.
    '''
    with app.app_context():
        db.create_all()

        _init_database(db)
        yield db

        db.drop_all()
        db.session.commit()

@pytest.fixture(scope='class')
def stats():
    class StatisticsActions:

        def __init__(self):
            self.client = None

        def get_statistics_by_id(self, userid):
            assert self.client is not None

            return self.client.get(f'/stats/{userid}')
            
    return StatisticsActions()

@pytest.fixture('class')
def jwt_token(app):

    class JWTActions():

        def create_token(self, identity, refresh=False, max_age=None):
            with app.app_context():
                if refresh:
                    return jwt.create_refresh_token(identity,
                                                    expires_delta=max_age)
                return jwt.create_access_token(identity,
                                               expires_delta=max_age)

        def set_token(self, response, token, refresh=False):
            with app.app_context():
                if refresh:
                    jwt.set_refresh_cookies(response, token)
                else:
                    jwt.set_access_cookies(response, token)

        def token_headers(self, identity, refresh=False, max_age=None):
            with app.app_context():
                token = self.create_token(identity, max_age=max_age)
                res = jsonify({})
                self.set_token(res, token)
                if refresh:
                    token = self.create_token(
                        identity, refresh=True, max_age=max_age)
                    self.set_token(res, token, refresh=True)
                return res.headers['Set-Cookie']

    return JWTActions()