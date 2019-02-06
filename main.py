import requests
from bs4 import BeautifulSoup
import json

url = "http://aviso.informador.com.mx/index.php/bienes_raices/busqueda?selecciono=1&ciudad_autocomplete=0&colonia_autocomplete=&transaccion=1&tipo=1&consulta=Zona+Metropolitana&precio_min=min&precio_max=max&recamaras_min=0&recamaras_max=0&metros_min=0&metros_max=0&quick-search=Zona+metropolitana-&quick-searchZap=Zapopan-3&quick-searchGdl=Guadalajara-2&quick-searchTlaq=Tlaquepaque-5&quick-searchTon=Tonal%C3%A1-4"
encoding = "utf-8"
r = requests.get(url)

# print(r.text)
soup = BeautifulSoup(r.text, "html.parser")

# print(soup)
items = soup.find_all(class_="items")

# print(items)

casas = items[0].find_all("li")
lista = []
for c in casas:
    casa = {
        "ubicacion" : c.find(class_ = "location").text,
        "titulo":c.a.text,
        "precio" : c.h5.text,
        "descripcion": c.p.text,
        "recamaras":c.find(class_="info-rec").text,
        "m2" : c.find(class_ = "info-m2").text,
        "m2_2" : c.find(class_ = "info-m2-2").text,
        "wc" : c.find(class_ = "info-wc").text,
        "cars" : c.find(class_ = "info-cars").text,
        "colonia" : c.find(class_ = "info-gps").contents[1],
        "imgs" : ['http' + i['src'] for i in c.find_all(['img'])]

    }
    lista.append(casa)

with open('informador.json', "w") as archivo:
    json.dump(lista,archivo, sort_keys=False,indent=4)

#print(lista)

paginas = soup.find(class_ = "pagination")
paginas = paginas.find_all('li')
urls = []
i = 2
while i < len(paginas) - 1:
    urls.append(paginas[i].a['href'])
    i = i + 1

print(urls)