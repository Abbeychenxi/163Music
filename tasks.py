import time
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')


@celery.task
def get_playlist():
    pass
