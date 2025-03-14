from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello World!"

@app.route('/login')
def login():
    return login.html
from controller import *
