import pandas as pd
import json
import jsonpickle



class ItemDTO:
    nummer = 17
    tconst = "nab17"
    def dump(self):
        return {'nummer': self.nummer,
               'tconst': self.tconst}

def vanmij():
    lijst = pd.read_csv("min_ages.csv")
    print(lijst)
    newlijst = pd.DataFrame()
    counter = 0
    for i,x in lijst.iterrows():
        if counter == 10:
            break;
        newlijst.loc[len(newlijst), ['tconst','min_age']] = x["tconst"],x["min_age"]
        counter += 1
    return newlijst.to_json() 

def nogeen(request):
    print("in de post")
    if request.method == 'POST':
        print(request.get_json()["een"])
        return "dit is echt de post"
    return "geen post"

def vanmij2():
    lijst = pd.read_csv("min_ages.csv")
    print(lijst)
    newlijst = pd.DataFrame()
    counter = 0
    for i,x in lijst.iterrows():
        if counter == 10:
            break;
        newlijst.loc[len(newlijst), ['tconst','min_age']] = x["tconst"],x["min_age"]
        counter += 1
    return newlijst.to_json(orient = "records")

def vanmij3():
    lijst = pd.read_csv("min_ages.csv")
    newlijst = pd.DataFrame(columns=['tconst', 'min_age'])
    counter = 0
    for i,x in lijst.iterrows():
        if counter == 10:
            break
        newlijst.loc[counter] = [x["tconst"], x["min_age"]]   
        counter += 1
    print(newlijst)
    return newlijst.to_json(orient = "records")

def vanmij4():
    lijst = pd.read_csv("min_ages.csv")
    newlijst = []
    counter = 0
    for i,x in lijst.iterrows():
        if counter == 10:
            break
        newlijst.append(ItemDTO())   
        counter += 1
    print(pd.DataFrame(newlijst).to_json(orient = "values"))
 #   return newlijst.to_json(orient = "records")


def vanmij5():
    lijst = pd.read_csv("min_ages.csv")
    newlijst = []
    counter = 0
    for i,x in lijst.iterrows():
        if counter == 10:
            break
        newlijst.append(ItemDTO()) 
        counter += 1

    ab = pd.DataFrame([[p.nummer, p.tconst] for p in newlijst], columns=list(['Ene','Andere']))
    return ab.to_json(orient = "records")


