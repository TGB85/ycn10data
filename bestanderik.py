import pandas as pd
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy import text

def hallo():
    return("hallo!")

def connect_to_db():
    engine = create_engine(
    "mysql+mysqlconnector://root@localhost/yc202210", echo=False, future=True)
    return engine

def connect_to_db_online():
    url = sqla.engine.URL.create(
        drivername='mysql+mysqlconnector',
        username="rootadmin",
        password="abcd1234ABCD!@#$",
        host="yc2210netflixdbpython.mysql.database.azure.com",
        database="recepten"
    )
    engine = create_engine(
    url, echo=False, future=True)
    return engine

def make_query(filter):
    where_clause = ''
    for k,v in filter.items():
        where_clause += f' {k} = {v} AND'
    where_clause = where_clause[0:-3]
    query = f'SELECT * FROM `recepten` WHERE {where_clause}'
    return query

def query_sql(query_text):
    engine = connect_to_db_online()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))
    return pd.DataFrame(query.fetchall())

def recepten(filters):
    q = make_query(filters)
    print(q)
    df = query_sql(q)
    print(df)
    return df.to_json(orient="records")

if __name__ == '__main__':
    a = connect_to_db_online()
    print(a)
    b = recepten({'vegetarisch':1})
    print(b)