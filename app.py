import os
from flask import Flask
from flask import render_template

from pymongo import MongoClient

# DB_URL = $SCALINGO_POSTGRESQL_URL

client = MongoClient(MONGO_URL)

db = client.test

print(db.name) 

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
