from __future__ import absolute_import, unicode_literals
#from celery import Celery
from celery import shared_task

#app = Celery('tasks', backend='rpc://', broker=f'amqp://guest:guest@rabbit:5672//')

#@app.task
#def startAPI(x):
#    return x

@shared_task
def startAPI(x):
    return x
