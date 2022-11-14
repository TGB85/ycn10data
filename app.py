from flask import Flask, request, jsonify
from Julio import julio
import json
import bestanderik
#import endpointerik
import endpointtamara
from roelien import roelien
# import felixbestand
#Voor nu uigecomment
# import scrappen
#import victorbestand
#from roelien import functieOefening

app = Flask(__name__)

@app.route("/")
def posters():
    return endpointtamara.three_posters()

@app.route("/dorine")
def select_movies():
    return endpointtamara.voor_dorine()

@app.route("/roelien")
def test_roelien():
    return roelien()

@app.route("/julioTest1")
def julioFunctie():
    return julio()

@app.route("/erik")
def endpointerik():
    return bestanderik.hallo()

@app.route("/erik2/", methods=["POST"])
def endpointerik2():
    post = request.json
    #print(post)
    res = bestanderik.recepten(post)
    return res

@app.route("/een_recept/<int:i>")
def endpointerik3(i):
    return bestanderik.een_recept(i)

@app.route("/drie_recepten/", methods=["POST"])
def endpointerik4():
    post = request.json
    #print(post)
    res = bestanderik.drie_recepten(post)
    return res

@app.route("/random_recept/")
def endpointerik5():
    return bestanderik.random_recept()

# @app.route("/crypto")
# def endpoint_crypto():
#     return scrappen.return_database()

@app.route("/endpointtamara/<int:genre_id>")
def movies(genre_id):
    print(f"genre_id = {genre_id}")
    return endpointtamara.three_movies_per_genre(genre_id)

@app.route("/filters/<rating>/<min_age>/<excl_genres>")
def get_filters(rating, min_age, excl_genres):
        return endpointtamara.filter_online_db(rating, min_age, excl_genres)

@app.route("/filters/<rating>/<min_age>/<excl_genres>/<incl_groups>")
def get_filtered(rating, min_age, excl_genres, incl_groups):
    return endpointtamara.filter_include(rating, min_age, excl_genres, incl_groups)

@app.route('/filter_movies', methods=['POST', 'GET'])
def filter_and_include():
    if request.method == 'POST':
        data = json.loads(request.data)
        rating = data['rating']
        min_age = data['min_age']
        excl_genres = data['excl_genres'] 
        if 'incl_groups' in data.keys():
            incl_groups = data['incl_groups']
            return endpointtamara.filter_include(rating, min_age, excl_genres, incl_groups)
        else:
            return endpointtamara.filter_online_db(rating, min_age, excl_genres)
    return "POST 'rating', 'min_age' and 'excl_genres', optional 'incl_groups'."

# @app.route("/checkfelix")
# def functiefelix1():
#     return felixbestand.vanmij5()

# @app.route("/checkfelix2", methods = ['GET', 'POST'])
# def functiefelix2():
#     return felixbestand.nogeen(request)