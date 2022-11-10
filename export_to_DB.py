import pandas as pd
#import mysql.connector
import sqlalchemy
import json


engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://root@localhost/yc202210", echo=False, future=True
)

for i in range(0,12):
    start = 20*i
    end = 20*(i+1)
    df = pd.read_csv(f"ah_recipes_{start}-{end}.csv")
    df = df[['titel','ingredienten','bereidings_stappen','img']]
    df['ingredienten'] = df['ingredienten'].apply(json.dumps)
    df['bereidings_stappen'] = df['bereidings_stappen'].apply(json.dumps)
    df.to_sql("recepten_details",engine,if_exists="append",index=False)


df = pd.read_csv("ah_recipes_240-258.csv")
print(df.columns)
df = df[['titel','ingredienten','bereidings_stappen','img']]
df['ingredienten'] = df['ingredienten'].apply(json.dumps)
df['bereidings_stappen'] = df['bereidings_stappen'].apply(json.dumps)
df.to_sql("recepten_details",engine,if_exists="append",index=False)


