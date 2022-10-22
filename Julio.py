import pandas as pd


def julio():
    print ("hoi")
    df = pd.read_csv("resourcesab/netflix_titles.csv")
    print (df)
    print (df.columns)
    #f = open("netflixDB.txt", "w")
    for m in df["title"]:
        print (m)
        #m = str(m)+"\n"
        #f.write(m)

    #f.close()

    #open and read the file after the appending:
    #f = open("netflixDB.txt", "r")
    #print(f.read())
    return "klein beetje insparatie!"



