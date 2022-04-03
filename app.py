import os
from flask import Flask
from flask import render_template

from pymongo import MongoClient

MONGO_URL = "mongodb://celery-bitters-8640:8P6lfFk5L6v-V-uqYT73@ec50dbe1-ac81-45a6-84fa-9ce2354aae20.celery-bitters-8640.mongo.a.osc-fr1.scalingo-dbs.com:32787/celery-bitters-8640?replicaSet=celery-bitters-8640-rs0&ssl=true"

client = MongoClient(MONGO_URL)

db = client.test

print(db.name) 
print("got to here")

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
