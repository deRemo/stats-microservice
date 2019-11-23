# -*- coding: utf-8 -*-
from celery import Celery
from flask import Flask
import stats
import json

from stats.extensions import db, celery, cache
from stats.api.search import search

__all__ = ('create_app', 'create_celery')

# Import blueprints and insert in the list
BLUEPRINTS = (search)


def create_app(config='config.py', app_name='search', blueprints=None):
    app = Flask(app_name)

    if config:
        app.config.from_pyfile(config)

    if blueprints is None:
        blueprints = BLUEPRINTS

    create_celery(app)
    build_blueprints(app, blueprints)
    db.init_app(app)
    celery.config_from_object(app.config)

    cache.init_app(app, config={'CACHE_TYPE': app.config['CACHE_TYPE']})
    
    return app


def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def build_blueprints(app, blueprints):
    if type(blueprints) != list:
        app.register_blueprint(blueprints)
    else:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
