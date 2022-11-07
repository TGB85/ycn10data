from flask import Flask, request
from Julio import julio
from endpoint_erik import leuke_functie
import endpointtamara
# import felixbestand
import scrappen
from flask import request
import victorbestand
from roelien import functieOefening

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
def functieOefening2():
    return functieOefening()

@app.route("/victorbestand2")
def hallotest():
    return victorbestand.hallo()

@app.route("/julioTest1")
def julioFunctie():
    return julio()

@app.route("/erik")
def endpoint_erik():
    return leuke_functie()

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



# @app.route("/checkfelix")
# def functiefelix1():
#     return felixbestand.vanmij5()

# @app.route("/checkfelix2", methods = ['GET', 'POST'])
# def functiefelix2():
#     return felixbestand.nogeen(request)



