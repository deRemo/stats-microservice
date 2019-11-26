import requests
from requests.exceptions import Timeout

from flask import current_app as app

from stats.models import Stats
from stats.extensions import celery, db


@celery.task
def poll_inconsistent():
    try:
        response = requests.get(f'{app.config["STORIES_ENDPOINT"]}/stories/stats')
    except Timeout:
        return
    
    to_update = response.json()
    for author in to_update:
        auth_stats = Stats.query.get(int(author))
        add = auth_stats is None
        if auth_stats is None:
            auth_stats = Stats()
        
        for story in to_update[author]:
            if story['dice'] != -1:
                auth_stats.n_dice += story['dice']
                auth_stats.stories_written += 1

            auth_stats.likes += story['likes']
            auth_stats.dislikes += story['dislikes']

        if add:
            db.session.add(auth_stats)

    db.session.commit()


@celery.task
def poll_refresh():
    try:
        response = requests.get(f'{app.config["STORIES_ENDPOINT"]}/stories/stats/refresh')
    except Timeout:
        return
    
    to_update = response.json()
    for author in to_update:
        auth_stats = Stats.query.get(int(author))

        add = auth_stats is None
        if auth_stats is None:
            auth_stats = Stats()

        auth_stats.n_dice = 0
        auth_stats.stories_written = 0
        auth_stats.likes = 0
        auth_stats.dislikes = 0

        for story in to_update[author]:
            auth_stats.n_dice += story['dice']
            auth_stats.stories_written += 1
            auth_stats.likes += story['likes']
            auth_stats.dislikes += story['dislikes']

        if add:
            db.session.add(auth_stats)

    db.session.commit()  
