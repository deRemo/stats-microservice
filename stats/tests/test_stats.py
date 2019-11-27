import datetime as dt
import pytest
from stats.models import Stats
from sqlalchemy.exc import IntegrityError
from stats.tasks import poll_inconsistent


@pytest.fixture
def init_database(database):
    example = Stats()
    example.author_id = 1
    example.likes_received = 5
    example.dislikes_received = 3
    example.stories_written = 15
    example.n_dice = 4
    database.session.add(example)

    database.session.commit()


class TestStats:
    def test_stats(self, app, client, statistics, init_database):
        statistics.client = client
        reply = statistics.get_statistics_by_id(1)

        assert reply.status_code == 200

class TestPolling:

    def test_poll_inconsistent(self, app, client, init_database, requests_mock):
        requests_mock.get(
            f'{app.config["STORIES_ENDPOINT"]}/stories/stats',
            status_code=200,
            json={
                '1': [{'dice': 4, 'likes': 0, 'dislikes': 0}, {'dice': -1, 'likes': 1, 'dislikes': 1}],
                '2': [{'dice': 3, 'likes': 1, 'dislikes': 1}]
            }
        )

        poll_inconsistent()

        usr1 = Stats.query.get(1)
        assert usr1.likes_received == 5
        assert usr1.dislikes_received == 4
        assert usr1.stories_written == 16
        assert usr1.n_dice == 5

        usr2 = Stats.query.get(2)
        assert usr2.likes_received == 1
        assert usr2.dislikes_received == 1
        assert usr2.stories_written == 1
        assert usr2.n_dice == 3
