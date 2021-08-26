import requests
import os
import tqdm
import json
from bs4 import BeautifulSoup 

URL_main = 'http://www.fundacionmemoriadelchamame.com'
#Division por orden alfabetico
URL_letras =  'http://www.fundacionmemoriadelchamame.com/letras/'

#Primer scrap para obtener los links de cada letra indice
request_main = requests.get(URL_letras)
soup = BeautifulSoup(request_main.content, 'html.parser')
botones =  soup.find_all(class_='btn btn-primary', type='button')
letras_lista = []

for boton in botones:
    if boton['href'] == '/letras/%C3%91/':
        letras_lista.append('/letras/Ñ/')
    else: 
        letras_lista.append(boton['href'])

#Armo una funcion que dada una letra, obtenga todos los
#links de pdf incluidos en esa clasificacion
def get_pdf_links(letra, pdf_links):
    URL_letra = URL_main + letra
    request = requests.get(URL_letra)
    soup = BeautifulSoup(request.content, 'html.parser')
    titulos = soup.find_all('div', id='my-gallery')
    for i in titulos[0]:
        if i.name == 'a':
            pdf_links.append(URL_main + i['href'])
    return i#pdf_links

#Paso esa funcion por todas las letras obtenidas
pdf_links = []
for letra in tqdm.tqdm(letras_lista):
    get_pdf_links(letra, pdf_links)

#guardo los links obtenidos en un archivo externo
with open('pdf_links.json', 'w') as f:
    json.dump(pdf_links, f, ensure_ascii=False, indent=4)
