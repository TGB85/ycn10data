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

@app.route("/dorine/<tekst>")
def select_movies(tekst):
    film = {"title": 'My Little Pony: A New Generation', "poster": 'https://m.media-amazon.com/images/M/MV5BOTY4ZmZjY2YtODg4ZS00YjlkLWJhOWMtMDU4Y2YyYjMwMDEzXkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_SX300.jpg', "plot": tekst}
    film2 = {"title":"Strictly Ballroom", "poster":"https://m.media-amazon.com/images/M/MV5BNjY2MWI2YWYtOGUyZS00ZGZjLTkyYjAtYWYxZDJmMzlkZjE0XkEyXkFqcGdeQXVyNTE1NjY5Mg@@._V1_SX300.jpg", "plot":tekst}
    film3 = {"title":"Man Up", "poster":"https://m.media-amazon.com/images/M/MV5BMTk4MjU0OTQ3Nl5BMl5BanBnXkFtZTgwMDM0MDM1NTE@._V1_SX300.jpg", "plot":tekst}
    films = [film, film2, film3]
    result = json.dumps(films)
    return json.loads(result)

@app.route("/dorine/<rating>/<min_age>/<excl_genres>/<int:genre_group>/<lang>")
@app.route("/dorine/<rating>/<min_age>/<excl_genres>/<int:genre_group>")
def three_movies(rating, min_age, excl_genres, genre_group, lang=''):
    return endpointtamara.filter_one_genre(rating, min_age, excl_genres, genre_group, lang)

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

@app.route("/genres")
def get_genre_list():
    return endpointtamara.get_genres()

@app.route("/genre_groups")
def genre_groups():
    return endpointtamara.get_genre_group()

@app.route("/languages")
def list_languages():
    return endpointtamara.get_languages()

@app.route("/min_age")
def age_categories():
    return endpointtamara.get_min_age()

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

@app.route("/filters/<rating>/<min_age>/<excl_genres>/<incl_groups>/<lang>")
def filter_lang(rating, min_age, excl_genres, incl_groups, lang):
    return endpointtamara.filter_include(rating, min_age, excl_genres, incl_groups, lang)

@app.route('/filter_movies', methods=['POST', 'GET'])
def filter_and_include():
    if request.method == 'POST':
        data = json.loads(request.data)
        rating = data.get('rating', 0)
        min_age = data.get('min_age', 14)
        excl_genres = data.get('excl_genres', "")
        lang = data.get('lang', "")
        if 'incl_groups' in data.keys():
            incl_groups = data['incl_groups']
            return endpointtamara.filter_include_arrays(rating, min_age, excl_genres, incl_groups, lang)
        else:
            return endpointtamara.filter_online_db(rating, min_age, excl_genres, lang)
    return "POST 'rating', 'min_age' and 'excl_genres', 'incl_groups' and 'lang'."

# @app.route("/checkfelix")
# def functiefelix1():
#     return felixbestand.vanmij5()

# @app.route("/checkfelix2", methods = ['GET', 'POST'])
# def functiefelix2():
#     return felixbestand.nogeen(request)