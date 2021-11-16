import requests
from functools import reduce
import operator
import pandas as pd





def geocode(direccion):
    """
    Esta función me da las coordenadas de la dirección concreta que le introduzca
    Arg: dirección ("string")
    Return: coordenadas
    """
    data = requests.get(f"https://geocode.xyz/{direccion}?json=1").json()
    try:
        return {"type": "Point", "coordinates": [data["latt"], data["longt"]]}
    except:
        return data


def getFromDict(diccionario,mapa):
    """
    Esta función la necesitaremos para extraer los key, values de los diccionarios que contienen
    la información requerida que nos da la API a la que llamamos. La usaremos dentro de una función
    posterior.
    """
    return reduce(operator.getitem,mapa,diccionario)

def type_point(lista):
    """
    Esta función la necesitaremos para conseguir la información de longitud y latitud con tipo 
    point, a partir de unas coordenadas que le introduzcamos. La usaremos dentro de una función
    posterior."""
    return {"type":"Point", "coordinates": lista}

def extraetodo(json):
    """
    Con esta función consigo una lista con cada uno de los diccionarios que contienen la información
    de nombre, latitud y longitud que necesito para generar mi dataframe.
    Arg: json
    Return: lista
    """
    todo = {"nombre": ["name"], "latitud": ["location", "lat"], "longitud": ["location", "lng"]} 
    total = []
    for elemento in json:
        libre = {key: getFromDict(elemento, value) for key,value in todo.items()}
        libre["location"] = type_point([libre["latitud"], libre["longitud"]])
        total.append(libre)
    return total

def suma_requisitos(df1,df2,df3,df4):
    """
    Esta función la utilizo para unir los 4 dataframe limpios que he creado para cada requerimiento
    elegido.
    Arg: 4 dataframes
    Return: 1 dataframe total
    """

    return pd.concat([df1, df2, df3, df4])



def normalizacion(df,col):

    """
    Con esta función consigo normalizar los datos de una columna de un dataframe.
    Arg: dataframe y columna concreta de este
    Return: lista de valores normalizados.
    """
    norm = []
    for i,row in df.iterrows():
        mini = df[col].min()
        maxi = df[col].max()
        norm.append((row[col]- mini)/(maxi-mini))
    return norm



def pesos(df):

    """
    Con esta función doy un peso concreto a cada uno de los requerimientos con los que estoy trabajando,
    itero por cada una de las categorías, y aplico el peso en base a la columna de datos normalizados.
    Arg: dataframe
    Return: lista
    """
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



        
def suma_final(df1,df2,df3):

    """
    Con esta función consigo un dataframe final, uniendo los dataframes de cada ciudad que contienen
    los datos normalizados y ponderados.
    Arg: 3 dataframe
    Return: 1 dataframe total final
    """
    return pd.concat([df1, df2, df3])