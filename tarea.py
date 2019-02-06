import requests
from bs4 import BeautifulSoup
import json

url = "http://www.cucei.udg.mx/directorio"

encoding = "utf8"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

items = soup.find_all(class_ = "item-list")

lista = []
for m in items:
    teach = {
        "dependencia":m.h3.text,
        "foto":m.find("img")['src'],
        "nombre":m.find(class_ = "views-field views-field-title").span.a.text,
        "puesto":m.find(class_ = "views-field views-field-field-puesto-directorio puesto-directorio").text[9:],
        "direccion":m.find(class_ = "views-field views-field-field-direcci-n direccion-directorio").text[12:],
        "teléfono":m.find(class_ = "views-field views-field-field-conmutador").text[12:]
    }

    lista.append(teach)

with open("maestros.json", "w", encoding=encoding) as archivo:
    json.dump(lista, archivo, sort_keys=False, indent=4,ensure_ascii=False)
