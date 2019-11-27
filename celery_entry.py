# -*- coding: utf-8 -*-
from stats.extensions import celery
from stats.tasks import poll_inconsistent, poll_refresh
from stats import create_app, create_celery

POLLING_RATE = 2.0

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(POLLING_RATE, poll_inconsistent.s(), name='story-microservice')

    #gather from story microservice
    sender.add_periodic_task(2000*POLLING_RATE, poll_refresh.s(), name='story-microservice')


app = create_app(config='config.py')
celery = create_celery(app)
celery.start()
