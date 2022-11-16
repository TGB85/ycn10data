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

sql_url = {'drivername': "mysql+mysqlconnector",
            'username': user,
            'password': pwd,
            'host': host,
            'database': database,
            'query':{"ssl_ca": "\DigiCertGlobalRootCA.crt.pem"}
            }

def get_connection():
    # return create_engine('mysql+mysqlconnector://%s:%s@yc2210netflixdbpython.mysql.database.azure.com/movies' %(quote(user), quote(pwd)),
	# 		connect_args=ssl_args, encoding='utf-8-sig')
    return create_engine(URL.create(**sql_url), encoding='utf-8-sig')            

def make_query(genre):
    return f'''
    SELECT movies.movie.title
    FROM movies.movie
    JOIN movies.movie_genre
        ON movies.movie.id = movies.movie_genre.movie_id
    WHERE genre_id = {genre};
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
    result = json.dumps(selection.title.to_dict())
    return result

def three_posters():
    query_text = '''
        SELECT movies.from_api.poster 
        FROM movies.from_api;
        '''
    data = query_sql(query_text)
    selection = data.sample(n=3)
    posters = [item for item in selection.poster]
    return f"<img src={posters[0]}><img src={posters[1]}><img src={posters[2]}>"

def filter_online_db(rating, min_age, excl_genres, lang=""):
    engine = get_connection()
    if len(lang) == 0:
        excl_lang = lang
    else:
        languages = lang.split(',') 
        if len(languages) == 1:
            excl_lang = f"AND movies.from_api.lang != '{languages[0]}'"
        else:
            excl_lang = f"AND movies.from_api.lang NOT IN {tuple(languages)}"
    query_text = f'''
    SELECT movies.movie.id,
        movies.movie.title, 
        movies.from_api.poster,
        movies.from_api.plot 
    FROM movies.movie
        JOIN movies.from_api
            ON movies.from_api.movie_id = movies.movie.id
        WHERE movies.movie.imdb_rating >= {rating}
            AND movies.movie.min_age <= {min_age}
            {excl_lang}
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
    return json.loads(json_obj)

def filter_include(rating, min_age, excl_genres, incl_groups, lang=""):
    engine = get_connection()
    genre_1, genre_2, genre_3 = incl_groups.split(',')
    if len(lang) == 0:
        excl_lang = lang
    else:
        languages = lang.split(',') 
        if len(languages) == 1:
            excl_lang = f"AND movies.from_api.lang != '{languages[0]}'"
        else:
            excl_lang = f"AND movies.from_api.lang NOT IN {tuple(languages)}"
    query_text = f'''
        SELECT movies.movie.id,
            movies.movie.title, 
            movies.from_api.poster,
            movies.from_api.plot 
        FROM
            (SELECT movies.movie.id FROM movies.movie
                WHERE movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_1})
                    AND movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_2})
                    AND movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                            JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                            WHERE group_id = {genre_3})
            UNION
            (SELECT movies.movie.id FROM movies.movie
                WHERE movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_1})
                    AND movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_2})
            ORDER BY RAND() DESC
            LIMIT 10)
            UNION
            (SELECT movies.movie.id FROM movies.movie
                WHERE movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id	
                                        WHERE group_id = {genre_1})
                    AND movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_3})
            ORDER BY RAND() DESC
            LIMIT 10)
            UNION
            (SELECT movies.movie.id FROM movies.movie
                WHERE movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_2})
                    AND movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_3})
            ORDER BY RAND() DESC
            LIMIT 10)
            ) three_genres

        JOIN movies.from_api ON movies.from_api.movie_id = three_genres.id
        JOIN movies.movie ON movies.movie.id = three_genres.id

        WHERE movies.movie.imdb_rating >= {rating}
            AND movies.movie.min_age <= {min_age}
            {excl_lang}
            AND movies.movie.id NOT IN (
                SELECT movie_id
                FROM movies.movie_genre
                JOIN movies.movie
                    ON movies.movie_genre.movie_id = movies.movie.id
                WHERE genre_id IN ({excl_genres})
                )
                
        ORDER BY RAND() DESC
        LIMIT 3;
        '''
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(query_text)
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result)

def filter_one_genre(rating, min_age, excl_genres, genre_group, lang=''):
    engine = get_connection()
    if len(lang) == 0:
        where_lang = lang
    else:
        languages = lang.split(',') 
        if len(languages) == 1:
            where_lang = f"AND movies.from_api.lang != '{languages[0]}'"
        else:
            where_lang = f"AND movies.from_api.lang NOT IN {tuple(languages)}"
    query_text = f'''
        SELECT movies.movie.id,
            movies.movie.title, 
            movies.from_api.poster,
            movies.from_api.plot 
        FROM
            (SELECT movies.movie.id FROM movies.movie
                WHERE movies.movie.id IN (SELECT movie_id FROM movies.movie_genre JOIN movies.movie ON movies.movie_genre.movie_id = movies.movie.id 
                                        JOIN movies.genre ON movies.movie_genre.genre_id = movies.genre.id
                                        WHERE group_id = {genre_group})
        ) one_genre

        JOIN movies.from_api ON movies.from_api.movie_id = one_genre.id
        JOIN movies.movie ON movies.movie.id = one_genre.id

        WHERE movies.movie.imdb_rating >= {rating}
            AND movies.movie.min_age <= {min_age}
            {where_lang}
            AND movies.movie.id NOT IN (
                SELECT movie_id
                FROM movies.movie_genre
                JOIN movies.movie
                    ON movies.movie_genre.movie_id = movies.movie.id
                WHERE genre_id IN ({excl_genres})
                )
                
        ORDER BY RAND() DESC
        LIMIT 3;
        '''
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(query_text)
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result)

def get_genres():
    engine = get_connection()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text('SELECT id, genre_text FROM movies.genre'))
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result)

def get_languages():
    engine = get_connection()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text('''
        SELECT lang FROM movies.from_api
        WHERE lang IS NOT NULL
        GROUP BY lang
        HAVING COUNT(*) > 10;'''))
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result) 

def get_min_age():
    engine = get_connection()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text('SELECT DISTINCT min_age FROM movies.movie'))
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result) 

def get_genre_group():
    engine = get_connection()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text('SELECT DISTINCT group_id, group_text FROM movies.genre WHERE group_id IS NOT NULL'))
    result = json.dumps([(dict(row._mapping.items())) for row in query])
    return json.loads(result) 

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    # print(three_movies_per_genre(genre_id=1))
    # print(three_posters())
    # print(filter_online_db(5.0,  14, '9,0'))
    # print(filter_online_db(5.0,  14, '9,0', "South_Asian"))
    # print(filter_online_db(5.0,  14, '9,0', "South_Asian,East_Asian"))
    # print(filter_include(rating=7.0, min_age=14, excl_genres='9', incl_groups='0,4,7'))
    # print(filter_include(rating=7.0, min_age=14, excl_genres='9', incl_groups='0,4,7', lang="East_Asian"))
    # print(filter_include(rating=5.0, min_age=18, excl_genres='9', incl_groups='0,4,7', lang="East_Asian,South_Asian"))
    # print(get_genres())