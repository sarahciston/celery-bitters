import celery
import os
# from dotenv import load_dotenv
# load_dotenv(./.env)

app = celery.Celery('nodeserver')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
@app.task
def hello(name):
    return "Hello "+name
