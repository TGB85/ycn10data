from flask import Flask
from julio import julio
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/julioTest1")
def julio():
    return julio()