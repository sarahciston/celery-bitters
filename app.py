import os
from pydoc import render_doc
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

import scal_task

app = Flask(__name__)

import datetime
import pymongo

SCALINGO_MONGO_URL = os.environ.get('SCALINGO_MONGO_URL') 

client = pymongo.MongoClient(SCALINGO_MONGO_URL)
# , tls=True, tlsAllowInvalidCertificates=True, tlsCAFile='mongo/ca.pem')

# client = pymongo.MongoClient(SCALINGO_MONGO_URL, tlsCAFile='mongo/ca.pem')
# client = pymongo.MongoClient('localhost', 27017)

db = client['ivo']
table = db['phrases']

print(client.list_database_names())
print(db.list_collection_names())

@app.route("/dbAdd")
def dbAdd():

    text = "testing one two three"

    newEntry = {
        "text": text,
        "machineGenerated": False,
        "createdAt": datetime.datetime.now().isoformat()
    }

    e = table.insert_one(newEntry)

    # return render(client.list_database_names())
    return e.inserted_id

@app.route("/")
def hello():
    name = request.args.get('name', 'John Doe')
    result = scal_task.hello.delay(name)
    result.wait()
    return render_template('index.html', celery=result)

@app.route("/test")
def test():
    info = request.args.get('name', 'default')
    result = scal_task.test.delay(name)
    result.wait()
    return render_template('index.html', celery=result)

@app.route("/clone") 
def clone():
    voice = request.args.get('voice')
    result = scal_task.clone.delay(voice)
    result.wait()
    return render_template('clone.html', celery=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
