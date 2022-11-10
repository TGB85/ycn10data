import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text, MetaData
import json
from urllib.parse import quote

# user = 'root'
# password = ''
# host = '127.0.0.1'
# port = 3306
# database = 'yc202210'

pwd='abcd1234ABCD!@#$'
ssl_args = {'ssl_ca': 
	'\DigiCertGlobalRootCA.crt.pem'}

def get_connection():
    return create_engine('mysql+mysqlconnector://rootadmin:%s@yc2210netflixdbpython.mysql.database.azure.com/movies' %quote(pwd),
				connect_args=ssl_args)

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

# def add_user(user_name):
#     if user_name:
#         query_text = f'''
#         INSERT INTO users (user_name)
#         VALUES ('{user_name}')
#         '''
#         engine = get_connection()
#         with engine.connect().execution_options(autocommit=True) as conn:
#             conn.execute(text(query_text))
#         print("user added")
#     print("no user added")

# def create_user_table():
#     engine = get_connection()
#     users = Table(
#         'users', meta,
#         Column('id', Integer, primary_key=True),
#         Column('user_name', String(12), index=True, unique=True)
#     )
#     meta.create_all(engine)

# create_user_table()
# df = pd.read_sql_query('''SELECT * FROM genres''', con=engine)
# print(df.head())

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    # print(three_movies_per_genre(genre_id=1))
    print(three_posters())


