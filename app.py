from flask import Flask

from Julio import julio

from endpoint_erik import leuke_functie
import endpointtamara


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/julioTest1")
def julio():
    return julio()

@app.route("/erik")
def endpoint_erik():
    return leuke_functie

@app.route("/helloworld2")
def hello_world2():
    return "<p>Hello, World nummer 2!</p>"

@app.route("/helloworld3")
def hello_world3():
    return "<p>Hello, World nummer 3!</p>"

@app.route("/endpointtamara")
def functie2():
    return endpointtamara.function_tamara()


