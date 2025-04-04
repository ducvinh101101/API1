from flask import Flask
hostlocal = "http://127.0.0.1:5000"
app = Flask(__name__)
@app.route('/')
def index():
    return "Hello World!"

@app.route('/login')
def login():
    return login.html
from controller import profile_controller, model_blood

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

