import pandas as pd


def julio():
    print("test")
    #mijnbestand is een variable
    mijnbestand = pd.read_csv("netflix_imdb.csv")

    #print(mijnbestand)

    #print(mijnbestand.columns)

    #print(mijnbestand["title"])

    #tellen van IMDB
    IMDB9 = 0

    alleFilms = []
    #iterrows itereert over de rows
    for index, films in mijnbestand.iterrows():
        if(films["rating"] == "PG-13"):
            alleFilms.append(films["title"])
        else:
            alleFilms.append(films["title"] + "===geen PG-13===")
        if(films["averageRating"] == 9):
            IMDB9 = IMDB9 + 1
            alleFilms.append("<<<<<<<<<<<<<<<<<<IMDB 9>>>>>>>>>>>>>>>>>>>>>")

        # print(IMDB9)
        # print(len(alleFilms))
    
    return pd.DataFrame(alleFilms).to_json(orient = "values")
    #return alleFilms
    #return "abc"
#julio()
#     #print ("hoi")
# df = pd.read_csv("resourcesab/netflix_titles.csv")
#     print (df)
#     print (df.columns)
#     #f = open("netflixDB.txt", "w")
#     for m in df["title"]:
#         print (m)
#         #m = str(m)+"\n"
#         #f.write(m)

#     #f.close()

#     #open and read the file after the appending:
#     #f = open("netflixDB.txt", "r")
#     #print(f.read())
#     return "klein beetje insparatie!"

# print(julio())

