import os
from flask import Flask
from flask import render_template
from flask import request

import scal_task

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get('name', 'John Doe')
    result = scal_task.hello.delay(name)
    result.wait()
    return render_template('index.html', celery=result)

@app.route('/public')


@app.route("/test")
def test():
    info = request.args.get('info', 'default')
    result = scal_task.test.delay(info)
    result.wait()
    return print(celery=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
