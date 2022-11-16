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

class Film:
    title = 'hoi'
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@app.route("/tweede/<tekst>")
def hello_world2(tekst):
    mijnfilm = Film()
    mijnfilm.title = tekst
    mijnfilm.poster = 'https://m.media-amazon.com/images/M/MV5BOTY4ZmZjY2YtODg4ZS00YjlkLWJhOWMtMDU4Y2YyYjMwMDEzXkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_SX300.jpg'
    mijnfilm.plot = 'After the time of the Mane 6, Sunny--a young Earth Pony--and her new Unicorn friend Izzy explore their world and strive to restore Harmony to Equestria'
    return mijnfilm.toJSON()

@app.route("/dorine/<tekst>")
def select_movies(tekst):
    film = {"tekst": tekst, "title": 'My Little Pony: A New Generation', "poster": 'https://m.media-amazon.com/images/M/MV5BOTY4ZmZjY2YtODg4ZS00YjlkLWJhOWMtMDU4Y2YyYjMwMDEzXkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_SX300.jpg', "plot": 'After the time of the Mane 6, Sunny--a young Earth Pony--and her new Unicorn friend Izzy explore their world and strive to restore Harmony to Equestria.'}
    film2 = {'tekst': tekst, "title":"Strictly Ballroom", "poster":"https://m.media-amazon.com/images/M/MV5BNjY2MWI2YWYtOGUyZS00ZGZjLTkyYjAtYWYxZDJmMzlkZjE0XkEyXkFqcGdeQXVyNTE1NjY5Mg@@._V1_SX300.jpg", "plot":"A maverick dancer risks his career by performing an unusual routine and sets out to succeed with a new partner."}
    film3 = {'tekst': tekst, "title":"Man Up", "poster":"https://m.media-amazon.com/images/M/MV5BMTk4MjU0OTQ3Nl5BMl5BanBnXkFtZTgwMDM0MDM1NTE@._V1_SX300.jpg", "plot":"Martin, a 19-year-old slacker, has his life turned upside down when he gets his Mormon girlfriend pregnant, so he moves in with his stoner best friend Randall, who teaches him to be a man."}
    films = [film, film2, film3]
    result = json.dumps(films)
    print(result)
    return json.loads(result)

select_movies('test')

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
        lang = data.get('lang')
        if 'incl_groups' in data.keys():
            incl_groups = data['incl_groups']
            return endpointtamara.filter_include(rating, min_age, excl_genres, incl_groups, lang)
        else:
            return endpointtamara.filter_online_db(rating, min_age, excl_genres)
    return "POST 'rating', 'min_age' and 'excl_genres', optional 'incl_groups'."

# @app.route("/checkfelix")
# def functiefelix1():
#     return felixbestand.vanmij5()

# @app.route("/checkfelix2", methods = ['GET', 'POST'])
# def functiefelix2():
#     return felixbestand.nogeen(request)