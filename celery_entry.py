# -*- coding: utf-8 -*-
from flask import current_app as app
import requests
from requests.exceptions import Timeout
from stats import create_app, create_celery
from stats.models import Stats

app = create_app(config='./stats/config.py')
celery = create_celery(app)

POLLING_RATE = 2.0

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(POLLING_RATE, poll_inconsistent.s(), name='story-microservice')

    #gather from story microservice
    sender.add_periodic_task(2000*POLLING_RATE, poll_refresh.s(), name='story-microservice')


@celery.task
def poll_inconsistent():
    received = False
    while not received:
        try:
            response = requests.get(f'{app.config["STORIES_ENDPOINT"]}/stories/stats')
            received = True
        except Timeout:
            pass
    
    to_update = response.json()
    for author in to_update:
        auth_stats = Stats.query.get(int(author))
        add = auth_stats is None
        if auth_stats is None:
            auth_stats = Stats()
        
        for story in to_update[author]:
            if story['dice'] != -1:
                auth_stats.n_dice += story['dice']

            auth_stats.likes += story['likes']
            auth_stats.dislikes += story['dislikes']

        if add:
            db.session.add(auth_stats)

    db.session.commit()


@celery.task
def poll_refresh():
    received = False
    while not received:
        try:
            response = requests.get(f'{app.config["STORIES_ENDPOINT"]}/stories/stats')
            received = True
        except Timeout:
            pass
    
    to_update = response.json()
    for author in to_update:
        auth_stats = Stats.query.get(int(author))
        add = auth_stats is None
        if auth_stats is None:
            auth_stats = Stats()
        else:
            auth_stats.n_dice = 0
            auth_stats.stories_written = 0
            auth_stats.likes = 0
            auth_stats.dislikes = 0
        
        for story in to_update[author]:
            if story['dice'] != -1:
                auth_stats.n_dice += story['dice']
                auth_stats.stories_written += 1

            auth_stats.likes += story['likes']
            auth_stats.dislikes += story['dislikes']

        if add:
            db.session.add(auth_stats)

    db.session.commit()  

celery.start()
