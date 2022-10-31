from multiprocessing import Value
from unicodedata import decimal
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import mysql.connector 
import pandas as pd

dbverbinding = mysql.connector.connect(
    host='localhost',
    port='3306',
    # user='Victor',
    # password='Victor',
    # database='coinmarketcap'
    database='yc202210',
    user='root',
    password=''
)

mijncursor = dbverbinding.cursor()
def return_database():

    

    mijncursor.execute("SELECT * FROM crypto")

    lijst = mijncursor.fetchall()
    return pd.DataFrame(lijst).to_json(orient = "records")

#print(allecoins)

pagina = requests.get('https://coinmarketcap.com/')

#print(pagina.content)

heeldehtml = BeautifulSoup(pagina.content, 'html.parser')

tabel = heeldehtml.find('tbody')

#print(tabel.prettify())

allerijen = tabel.find_all('tr')
print(len(allerijen))
alleCoinNames = []
alleMarketCaps = []

#x = 0
for rij in allerijen:
#for x in range(50):
    #x = x + 1
    #print(rij)
    #rij = allerijen[x]
    cel = rij.find(class_="sc-14rfo7b-0 lhJnKD")
    if cel is not None:    
        alleCoinNames.append(cel.text)
        #if x > 50:
            #break
#y = 0
#for rij in allerijen:
for y in range(50):
    #y = y + 1
    #print(rij)
    rij = allerijen[y]
    cel = rij.find(class_="sc-1ow4cwt-1") 
    if cel is not None: 
         
        alleMarketCaps.append(cel.text)
        #if y > 50:
            #break


# i =0
# while i < len(alleMarketCaps):
#     sql = "INSERT INTO Crypto (Name, MarketCap) VALUES (%s, %s)"
#     Values = (alleCoinNames[i], alleMarketCaps[i])
#     mijncursor.execute(sql, Values)
#     dbverbinding.commit()
#     i += 1

# print(return_database())