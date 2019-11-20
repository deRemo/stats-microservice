# -*- coding: utf-8 -*-
import requests
from stats import create_app, create_celery

app = create_app(config='./stats/config.py')
celery = create_celery(app)

POLLING_RATE = 2.0

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(POLLING_RATE, poll_stories.s(), name='story-microservice')

    #gather from user microservice
    sender.add_periodic_task(POLLING_RATE, poll_users.s(), name='user-microservice')

    #gather from reaction microservice
    sender.add_periodic_task(POLLING_RATE, poll_reactions.s(), name='reaction-microservice')

@celery.task
def poll_stories():
    print("stories")
    #request at endpoint
    #retrieve results
    #call to async function that computes stats
    #requests.get('/stories')#(f'{app.config["SEARCH_ENDPOINT"]}/stories')


def poll_users():
    print("users")

def poll_reactions():
    print("reaction")

celery.start()
