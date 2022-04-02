import celery
import os
from pymongo import MongoClient

app = celery.Celery('scalingo-sample')

# app.config['CELERY_BROKER_URL'] = MONGODB_CON_STR
# app.config['CELERY_RESULT_BACKEND'] = MONGODB_CON_STR

app.conf.update(BROKER_URL=os.environ['MONGO_URL'],
                CELERY_RESULT_BACKEND=os.environ['MONGO_URL'])

db = MongoClient(MONGO_URL)[DB_NAME]

@app.task
def hello(name):
    return "Hello "+name
