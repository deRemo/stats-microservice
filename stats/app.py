# -*- coding: utf-8 -*-
from flask_jwt_extended import JWTManager
from celery import Celery
from flask import Flask
import stats
import json

from stats.extensions import db, celery, cache
from stats.api.stats import stats

__all__ = ('create_app', 'create_celery')

# Import blueprints and insert in the list
BLUEPRINTS = (stats,)


def create_app(config='config.py', app_name='stats', blueprints=None):
    app = Flask(app_name)

    if config:
        app.config.from_pyfile(config)

    if blueprints is None:
        blueprints = BLUEPRINTS

    jwt = JWTManager(app)
    create_celery(app)
    build_blueprints(app, blueprints)
    db.init_app(app)
    db.create_all(app=app)
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
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
