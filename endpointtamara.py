import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import text
import json
# from urllib.parse import quote
import os

user = os.getenv('DB_USERNAME')
pwd = os.getenv('DB_PASSWORD')
host = 'yc2210netflixdbpython.mysql.database.azure.com'
database = 'movies'

# ssl_args = {'ssl_ca': '\DigiCertGlobalRootCA.crt.pem'}
# create_engine('mysql+mysqlconnector://%s:%s@yc2210netflixdbpython.mysql.database.azure.com/movies' %(quote(user), quote(pwd)),
# 			connect_args=ssl_args, encoding='utf-8-sig')`

sql_url = {'drivername': "mysql+mysqlconnector",
            'username': user,
            'password': pwd,
            'host': host,
            'database': database,
            'query':{"ssl_ca": "\DigiCertGlobalRootCA.crt.pem"}
            }

def get_connection():
    return create_engine(URL.create(**sql_url), encoding='utf-8-sig')     
            

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
def filter_online_db(rating, min_age, excl_genres):
    engine = get_connection()
    # genres = excl_genres.split(',')
    # exclude = ''
    # for genre in genres[:-1]:
    #     exclude += f"movies_genres.genre_{genre} IS NULL AND "
    # exclude += f"movies_genres.genre_{genres[-1]} IS NULL"
    # slash=r'https://m.media-amazon.com/images/M/' # replace(movies.from_api.poster, "https://m.media-amazon.com/images/M/", "{slash}"), 
    query_text = f'''
    SELECT movies.movie.title, 
        movies.from_api.poster,
        movies.from_api.plot 
    FROM movies.movie
        JOIN movies.from_api
            ON movies.from_api.movie_id = movies.movie.id
        WHERE movies.movie.imdb_rating >= {rating}
            AND movies.movie.min_age <= {min_age}
            AND movies.movie.id NOT IN (
                SELECT movie_id
                FROM movies.movie_genre
                JOIN movies.movie
                    ON movies.movie_genre.movie_id = movies.movie.id
                WHERE genre_id IN ({excl_genres})
                );
    '''
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(query_text)
    data = pd.DataFrame(query.fetchall())
    json_obj = data.sample(n=3).to_json(orient = "records")
    # print(sample.poster)
    # json_obj = sample
    return json.dumps(json.loads(json_obj))

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    # print(three_movies_per_genre(genre_id=1))
    # print(three_posters())
    # print(filter_online_db(5.0,  14, '9,0'))


