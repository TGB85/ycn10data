import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

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

# engine = get_connection()
# df = pd.read_sql_query('''SELECT * FROM genres''', con=engine)
# print(df.head())

def make_query(genre):
    return f'''
    SELECT tconst FROM movies_genres
    WHERE genre_{genre} is not NULL;
    '''

def query_sql(query_text):
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))
    return pd.DataFrame(query.fetchall())

def function_tamara(genre_id=0):
    query_test = make_query(genre_id)
    data = query_sql(query_test)
    return data.head(3)

if __name__ == '__main__':
    try:
        engine = get_connection()
        print(f"Connection to {host} created.")
    except Exception as er_msg:
        print("Connection failed due to error: \n", er_msg)
    
    print(function_tamara(genre_id=1))


