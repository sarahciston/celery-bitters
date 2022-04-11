import celery
import os
# from decouple import config

# URL = os.environ['REDIS_URL']
# URL = config('REDIS_URL')

app = celery.Celery('scalingo-sample')


app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
@app.task
def hello(name):
    return "Hello "+name
