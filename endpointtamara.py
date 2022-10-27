import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import json

user = 'root'
password = ''
host = '127.0.0.1'
port = 3306
database = 'yc202210'

def get_connection():
    return create_engine(
        url="mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(
            host=host, db=database, user=user, pw=password)
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

# df = pd.read_sql_query('''SELECT * FROM genres''', con=engine)
# print(df.head())

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection to {host} created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    print(three_movies_per_genre(genre_id=1))
    print(three_posters())


