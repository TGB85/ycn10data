import pandas as pd
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy import text
import os
from decouple import config

def hallo():
    return("hallo!")

def connect_to_db():
    engine = create_engine(
    "mysql+mysqlconnector://root@localhost/yc202210", echo=False, future=True)
    return engine

def connect_to_db_online():
    try:
        username = os.getenv('DB_USERNAME')
    except:
        username = config('DB_USERNAME')
    try:
        password = os.getenv('DB_PASSWORD')
    except:
        password = config('DB_PASSWORD')
    url = sqla.engine.URL.create(
        drivername='mysql+mysqlconnector',
        username=username,
        password=password,
        host="yc2210netflixdbpython.mysql.database.azure.com",
        #database="recepten"
    )
    engine = create_engine(
    url, echo=False, future=True)
    return engine

def make_query(filter={}):
    where_clause = ''
    if filter == {}:
        return 'SELECT * FROM `recepten`.`recepten`'
    for k,v in filter.items():
        where_clause += f' {k} = {v} AND'
    where_clause = where_clause[0:-3]
    query = f'SELECT * FROM `recepten`.`recepten` WHERE {where_clause}'
    return query

def query_sql(query_text):
    engine = connect_to_db_online()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))
    return pd.DataFrame(query.fetchall())

def een_recept(i):
    df = query_sql(f'SELECT * FROM `recepten`.`recepten` WHERE id={i}')
    df2 = query_sql(f'SELECT * FROM `recepten`.`recepten_details` WHERE id={i}')
    res = pd.merge(df,df2,on='id')
    return res.to_json(orient="records")

def recepten(filters):
    q = make_query(filters)
    df = query_sql(q)
    return df.to_json(orient="records")

if __name__ == '__main__':
    a = een_recept(3)
    print(a)