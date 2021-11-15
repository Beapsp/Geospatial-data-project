import requests
from functools import reduce
import operator
import pandas as pd
from scipy.spatial import distance




def geocode(direccion):
    """
    Esta función saca las coordenadas de la dirección que le pases
    """
    data = requests.get(f"https://geocode.xyz/{direccion}?json=1").json()
    try:
        return {"type": "Point", "coordinates": [data["latt"], data["longt"]]}
    except:
        return data


def getFromDict(diccionario,mapa):
    return reduce(operator.getitem,mapa,diccionario)

def type_point(lista):
    return {"type":"Point", "coordinates": lista}

def extraetodo(json):
    todo = {"nombre": ["name"], "latitud": ["location", "lat"], "longitud": ["location", "lng"]} 
    total = []
    for elemento in json:
        libre = {key: getFromDict(elemento, value) for key,value in todo.items()}
        libre["location"] = type_point([libre["latitud"], libre["longitud"]])
        total.append(libre)
    return total

def suma_requisitos(df1,df2,df3,df4):
    return pd.concat([df1, df2, df3, df4])

def pesos(df):
    lista_pesos=[]
    for i,row in df.iterrows():   
        if row["categoria"] == "Disco":
            lista_pesos.append(row["Normalizado"]*0.2)
        elif row["categoria"] == "Airport":
            lista_pesos.append(row["Normalizado"]*0.4)
        elif row["categoria"] == "Vegan":
            lista_pesos.append(row["Normalizado"]*0.1)
        else: 
            lista_pesos.append(row["Normalizado"]*0.3)
    return lista_pesos


def normalizacion(df,col):
    norm = []
    for i,row in df.iterrows():
        mini = df[col].min()
        maxi = df[col].max()
        norm.append((row[col]- mini)/(maxi-mini))
    return norm
        
def suma_final(df1,df2,df3):
    return pd.concat([df1, df2, df3])