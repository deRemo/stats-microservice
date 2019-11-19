# -*- coding: utf-8 -*-
import requests
from service import create_app, create_celery

app = create_app(config='./service/config.py')
celery = create_celery(app)

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(2.0, get_story_stats.s(), name='story-microservice')

@celery.task
def get_story_stats():
    print("test")
    #requests.get('/stories')#(f'{app.config["SEARCH_ENDPOINT"]}/stories')


celery.start()
