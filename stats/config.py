# -*- coding: utf-8 -*-
#Flask
import os

SECRET_KEY = 'change me please'

USERS_ENDPOINT = os.getenv('USERS_API', 'localhost:5001')
STORIES_ENDPOINT = os.getenv('STORIES_API', 'localhost:5002')
REACTIONS_ENDPOINT = os.getenv('REACTIONS_API', 'localhost:5003')
STATISTICS_ENDPOINT = os.getenv('STATISTICS_API', 'localhost:5004')
AUTH_ENDPOINT = os.getenv('AUTH_API', 'localhost:5005')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Europe/London'

# JWT
SECRET_KEY = 'some-secret-string-CHANGE-ME'
JWT_SECRET_KEY = 'jwt-secret-string-CHANGE-ME'
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/auth/token_refresh'
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_SECURE = False  # True for only https

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///stats.db'

# Flask-Caching
CACHE_TYPE = 'redis'
