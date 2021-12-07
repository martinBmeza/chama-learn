import requests
import os
from tqdm import tqdm
import json
from bs4 import BeautifulSoup

def clean_letra(letra):
    cut_list = ['\r', 'I', 'II', '(estribillo)']
    for to_cut in cut_list:
        letra = letra.replace(to_cut, '')
    return letra

URL = 'https://www.cancioneros.com/letras/artista/12018/folklore-argentino'

# Obtengo los links de cada letra
request_main = requests.get(URL)
soup = BeautifulSoup(request_main.content, 'html.parser')
canciones =  soup.find_all('a')

links = []
for cancion in canciones:
    link = cancion.get('href')
    if 'cancion/' in link:
        links.append(link)

# scrapeo cada link para obtener titulo y letra
for link in tqdm(links):
    URL_letra = 'https://www.cancioneros.com/letras/' + link

    # Obtengo la letra
    request_main = requests.get(URL_letra)
    soup = BeautifulSoup(request_main.content, 'html.parser')
    letra =  soup.find_all(class_='lletra_can')[0].text.strip().replace('\r', '')
    letra = clean_letra(letra)
    titulo =  soup.find_all(class_="titol")[0].text

    # guardo cada letra en un archivo txt
    f = open('txts/'+titulo+'.txt', 'wb')
    f.write(letra.encode('utf8'))
    f.close()

