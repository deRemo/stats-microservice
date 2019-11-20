import json
import pytest

from service.app import create_app
from service.update_stats import init_stories_stats


@pytest.fixture
def app():
    app = create_app(config='tests/config_test.py')

    return app


@pytest.fixture
def client_factory(app):

    class ClientFactory:

        def __init__(self, app):
            self._app = app

        def get(self):
            return self._app.test_client()

    return ClientFactory(app)


@pytest.fixture
def client(app, client_factory):
    return client_factory.get()


@pytest.fixture
def auth():

    class AuthActions:

        def __init__(self):
            self.client = None

        def signup(self, data):
            assert self.client is not None
            return self.client.post('/signup',
                                    data=json.dumps(data),
                                    content_type='application/json')

        def login(self, data):
            assert self.client is not None
            return self.client.post('/login',
                                    data=json.dumps(data),
                                    content_type='application/json')

        def logout(self, login_token=None):
            assert self.client is not None
            if login_token is not None:
                return self.client.post('/logout',
                                        headers={'Set-Cookie': login_token})
            return self.client.post('/logout')

    return AuthActions()


class StatsActions:
    '''
    Class for stats management in the testing environment.
    '''

    def __init__(self, client):
        self._client = client

    def init_stories_stats(self, stories):
        return init_stories_stats(stories)


def update_stats(client):
    '''
    Provide stats functionalities
    '''
    return StatsActions(client)