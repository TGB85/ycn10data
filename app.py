from flask import Flask
from endpoint_erik import leuke_functie

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/erik")
def endpoint_erik():
    return leuke_functie