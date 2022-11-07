import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

def hallo():
    return("hallo!")

def connect_to_db():
    engine = create_engine(
    "mysql+mysqlconnector://root@localhost/yc202210", echo=False, future=True)
    return engine

def make_query(**filter):
    where_clause = ''
    for k,v in filter.items():
        where_clause += f' {v} AND'
    where_clause = where_clause[0:-3]
    query = f'SELECT * FROM `recepten` WHERE {where_clause}'
    return query

def query_sql(query_text):
    engine = connect_to_db()
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))
    return pd.DataFrame(query.fetchall())

def recepten(filters):
    q = make_query(a=filters)
    #print(q)
    df = query_sql(q)
    #print(df)
    return df.to_json()