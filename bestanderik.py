import pandas as pd
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy import text
import os
import random
try:
    from decouple import config
except:
    pass

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

def make_where(filter):
    where_clause = ''
    for k,v in filter.items():
        print(type(v))
        if type(v)==str:
            where_clause += f" {k} = '{v}' AND"
        elif type(v)==list:
            in_part = '('
            for j in v:
                in_part += f"'{j}',"
            in_part = in_part[:-1]+')'
            where_clause += f" {k} in {in_part} AND"
        else:
            where_clause += f' {k} = {v} AND'
    where_clause = where_clause[0:-3]
    return where_clause

def make_query(filter={}):
    if filter == {}:
        return 'SELECT * FROM `recepten`.`recepten`'
    where_clause = make_where(filter)
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

def random_recept():
    m = query_sql('SELECT MAX(id) AS m FROM `recepten`.`recepten`')['m'][0]
    i = random.randint(0,m)
    res = een_recept(i)
    return res

def recepten(filters):
    q = make_query(filters)
    df = query_sql(q)
    return df.to_json(orient="records")

def drie_recepten(filters):
    w = make_where(filters)
    print(w)
    df1 = query_sql(f'SELECT * FROM `recepten`.`recepten` WHERE {w} ORDER BY RAND() LIMIT 3')
    ids = list(df1['id'])
    df2 = query_sql(f'SELECT * FROM `recepten`.`recepten_details` WHERE id IN ({ids[0]},{ids[1]},{ids[2]}) ')
    res = pd.merge(df1,df2,on='id')
    return res.to_json(orient="records")

if __name__ == '__main__':
    #a = random_recept()
    #print(a)
    b = drie_recepten({'bbq':1,'zomer':1,'soort_recept':["pasta","rijst"]})
    print(b)