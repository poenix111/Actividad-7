import requests
import requests
from bs4 import BeautifulSoup
import json
import datetime 

class Informador:
    def __init__(self):
        self.lista = []

    def scrapping(self):
        url = "http://aviso.informador.com.mx/index.php/bienes_raices/busqueda?selecciono=1&ciudad_autocomplete=0&colonia_autocomplete=&transaccion=1&tipo=1&consulta=Zona+Metropolitana&precio_min=min&precio_max=max&recamaras_min=0&recamaras_max=0&metros_min=0&metros_max=0&quick-search=Zona+metropolitana-&quick-searchZap=Zapopan-3&quick-searchGdl=Guadalajara-2&quick-searchTlaq=Tlaquepaque-5&quick-searchTon=Tonal%C3%A1-4"
        r = requests.get(url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all(class_="items")
        casas = items[0].find_all("li")

        self.scrapping_casas(casas)
        paginas = soup.find(class_="pagination")
        paginas = paginas.find_all('li')
        urls = []
        i = 2
        while i < len(paginas) - 1:
            urls.append(paginas[i].a['href'])
            i = i + 1
        self.scrapping_paginas(urls)

    def scrapping_paginas(self, urls):
        for url in urls:
            r = requests.get(url)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all(class_="items")
            casas = items[0].find_all("li")
            self.scrapping_casas(casas)

    def scrapping_casas(self, casas):
        for c in casas:
            casa = {
                "ubicacion": c.find(class_="location").text,
                "titulo": c.a.text,
                "precio": c.h5.text,
                "descripcion": c.p.text,
                "recamaras": c.find(class_="info-rec").text,
                "m2": c.find(class_="info-m2").text,
                "m2_2": c.find(class_="info-m2-2").text,
                "wc": c.find(class_="info-wc").text,
                "cars": c.find(class_="info-cars").text,
                "colonia": c.find(class_="info-gps").contents[1],
                "imgs": ['http' + i['src'] for i in c.find_all(['img'])]

            }
            self.lista.append(casa)
    def to_json(self):
        with open('informador ' + datetime.datetime.now().strftime('%y-%m-%d')+ '.json', "w") as archivo:
            json.dump(self.lista,archivo, sort_keys=False,indent=4)