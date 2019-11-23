import datetime as dt
import pytest
from stats.models import Stats
from sqlalchemy.exc import IntegrityError

MOCK_STATS = dict(
    likes_given=2,
    dislikes_given=0,
    likes_received=5,
    dislikes_received=3,
    stories_written=15,
    avg_ndice=4.50,
    stories_per_day=2,
    date_of_entry=str(dt.datetime.now().date()),
    last_activity=str(dt.datetime.now().date()),
    is_active=True,
)

MOCK_AUTHOR_ID = 'author_id=1'

@pytest.fixture
def init_database(database):
    print("init database")
    try:
        example = Stats()
        example.author_id = 1
        example.likes_given = 2
        example.dislikes_given = 0
        example.likes_received = 5
        example.dislikes_received = 3
        example.stories_written = 15
        example.avg_ndice = 4.50
        example.stories_per_day = 2
        #example.date_of_entry = str(dt.datetime.now())
        #example.last_activity = str(dt.datetime.now())
        example.is_active = True
        database.session.add(example)

        database.session.commit()
    except IntegrityError as _:
        database.session.rollback()
    

class TestStats:
    def test_stats(self, app, client, stats, requests_mock, init_database):
        stats.client = client
        #reply = stats.get_statistics_by_id(1)

        #assert reply.status_code == 200