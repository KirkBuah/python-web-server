# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user')
def user():
    return 'Username'

if __name__ == '__main__':
    app.run(debug=True)
