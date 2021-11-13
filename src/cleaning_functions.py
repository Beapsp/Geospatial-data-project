import requests
from functools import reduce
import operator



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

def suma_requisitos(lista1,lista2,lista3,lista4):
    return [*lista1,*lista2,*lista3,*lista4]
    
