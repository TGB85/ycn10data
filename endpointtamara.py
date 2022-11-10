import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text, MetaData
import json
from urllib.parse import quote
import os

user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = 'yc2210netflixdbpython.mysql.database.azure.com'
database = 'movies'

ssl_args = {'ssl_ca': 
	'\DigiCertGlobalRootCA.crt.pem'}

def get_connection():
    return create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(host=host, db=database, user=user, pw=password)
            )
            

def make_query(genre):
    return f'''
    SELECT tconst FROM movies_genres
    WHERE genre_{genre} is not NULL;
    '''

def query_sql(query_text):
    engine = get_connection()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))
    query = get_connection().execute(text(query_text))
    return pd.DataFrame(query.fetchall())

def three_movies_per_genre(genre_id=0):
    query_test = make_query(genre_id)
    data = query_sql(query_test)
    selection = data.sample(n=3)
    result = json.dumps(selection.tconst.to_dict())
    return result

def three_posters():
    query_text = '''
        SELECT poster 
        FROM from_api;
        '''
    data = query_sql(query_text)
    selection = data.sample(n=3)
    posters = [item for item in selection.poster]
    return f"<img src={posters[0]}><img src={posters[1]}><img src={posters[2]}>"

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    # print(three_movies_per_genre(genre_id=1))
    print(three_posters())


