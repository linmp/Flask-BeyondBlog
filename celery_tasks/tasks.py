import time

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379/1')


@app.task
def add(x, y):
    for i in range(x):
        for j in range(y):
            h = i * j
    time.sleep(10)
    return h
