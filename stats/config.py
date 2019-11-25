# -*- coding: utf-8 -*-
#Flask
import os

DEBUG = True
SECRET_KEY = 'change me please'

USERS_ENDPOINT = os.getenv('USERS_API', 'localhost:5001')
STORIES_ENDPOINT = os.getenv('STORIES_API', 'localhost:5002')
REACTIONS_ENDPOINT = os.getenv('REACTIONS_API', 'localhost:5003')
STATISTICS_ENDPOINT = os.getenv('STATISTICS_API', 'localhost:5004')
AUTH_ENDPOINT = os.getenv('AUTH_API', 'localhost:5005')

# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Europe/London'

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///stats.db'

# Flask-Caching
CACHE_TYPE = 'redis'