import pandas as pd
#import mysql.connector
import sqlalchemy


engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://root@localhost/yc202210", echo=False, future=True
)

for i in range(0,12):
    start = 20*i
    end = 20*(i+1)
    df = pd.read_csv(f"ah_recipes_{start}-{end}.csv")
    print(df.columns)
    df = df[['titel', 'bereidingstijd', 'oventijd', 'aantal_personen',
       'rating', 'glutenvrij',
       'vegetarisch', 'lactosevrij', 'veganistisch', 'zonder_vlees_vis',
       'kerst', 'bbq', 'lente', 'zomer', 'herfst', 'winter', 'keuken1',
       'keuken2', 'soort_recept']]
    df.to_sql("recepten",engine,if_exists="append",index=False)


df = pd.read_csv("ah_recipes_240-258.csv")
print(df.columns)
df = df[['titel', 'bereidingstijd', 'oventijd', 'aantal_personen',
       'rating', 'glutenvrij',
       'vegetarisch', 'lactosevrij', 'veganistisch', 'zonder_vlees_vis',
       'kerst', 'bbq', 'lente', 'zomer', 'herfst', 'winter', 'keuken1',
       'keuken2', 'soort_recept']]
df.to_sql("recepten",engine,if_exists="append",index=False)

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "",
#     database="yc202210"
# )

