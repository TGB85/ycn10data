from flask import Flask
from Julio import julio
from endpoint_erik import leuke_functie
import endpointtamara
import felixbestand
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/julioTest1")
def julioFunctie():
    return julio()

@app.route("/erik")
def endpoint_erik():
    return leuke_functie()

@app.route("/helloworld2")
def hello_world2():
    return "<p>Hello, World nummer 2!</p>"

@app.route("/endpointtamara/posters")
def posters():
    return endpointtamara.three_posters()

@app.route("/endpointtamara/<int:genre_id>")
def movies(genre_id):
    print(f"genre_id = {genre_id}")
    return endpointtamara.three_movies_per_genre(genre_id)



@app.route("/checkfelix")
def functiefelix1():
    return felixbestand.vanmij5()

@app.route("/checkfelix2", methods = ['GET', 'POST'])
def functiefelix2():
    return felixbestand.nogeen(request)



