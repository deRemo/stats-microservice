# -*- coding: utf-8 -*-
from stats.tasks import poll_inconsistent, poll_refresh
from stats import create_app, create_celery

POLLING_RATE = 2.0

app = create_app(config='config.py')
celery = create_celery(app)

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(POLLING_RATE, poll_inconsistent.s(), name='poll-inconsistent')

    #gather from story microservice
    sender.add_periodic_task(2000*POLLING_RATE, poll_refresh.s(), name='refresh')


celery.start()
