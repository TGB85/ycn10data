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

@app.route("/", methods=['POST', 'GET'])
def add_username():
    if request.method == 'POST':
        user_name = request.form['user_name']
        print(user_name)
        endpointtamara.add_user(user_name)
        return f'<p>A new user added with username {user_name}</p>'
    return '''<form action='/' method = "post">
            <p>Enter username:</p>
            <p><input type="text" name="user_name" /></p>
            <p><button type="submit" value="submit" />Submit</p>
            </form>'''

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
    print(post)
    res = bestanderik.recepten(post)
    return res

@app.route("/een_recept/<int:i>")
def endpointerik3(i):
    return bestanderik.een_recept(i)

@app.route("/crypto")
def endpoint_crypto():
    return scrappen.return_database()

@app.route("/endpointtamara/posters")
def posters():
    return endpointtamara.three_posters()

@app.route("/endpointtamara/<int:genre_id>")
def movies(genre_id):
    print(f"genre_id = {genre_id}")
    return endpointtamara.three_movies_per_genre(genre_id)

@app.route("/filters/<rating>/<min_age>/<excl_genres>")
def get_filters(rating, min_age, excl_genres):
        return endpointtamara.filter_online_db(rating, min_age, excl_genres)

# @app.route("/checkfelix")
# def functiefelix1():
#     return felixbestand.vanmij5()

# @app.route("/checkfelix2", methods = ['GET', 'POST'])
# def functiefelix2():
#     return felixbestand.nogeen(request)