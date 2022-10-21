from flask import Flask
import endpointtamara

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/helloworld2")
def hello_world2():
    return "<p>Hello, World nummer 2!</p>"

@app.route("/helloworld3")
def hello_world3():
    return "<p>Hello, World nummer 3!</p>"

@app.route("/endpointtamara")
def functie2():
    return endpointtamara.function_tamara()
