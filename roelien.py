import pandas as pd


#def find_movie_genre(movie):
    #movie_list = pd.read_csv("movie_titles.csv")

    #movie = movie.lower().capitalize()

    #for movieitem in movie_list['title']:
        #if movie == movieitem:
            #print(movie)
            #return movie
        
    #return "Voer een film in"
    
#find_movie_genre("Titanic")



def geef_een_genre(genre):
    genre_list = pd.read_csv("genres.csv")

    genre = genre.lower().capitalize()

    for genre_naam in genre_list["genre"]:
        if genre_naam == genre:
            return genre

    return "Geef een genre mee"

print("Biography")

geef_een_genre("biography")
