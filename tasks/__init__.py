from core.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER
from celery import Celery



worker = Celery('worker', broker=f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}', include=['tasks.worker'])
beat = Celery('beat', broker=f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0', include=['tasks.beat'])
