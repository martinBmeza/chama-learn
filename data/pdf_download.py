import  tqdm
import json 
import urllib.request

#Cargo el archivo q contiene los links
archivo = open('pdf_links.json')
links = json.load(archivo)

#descargo los pdfs
def descargar_pdf(pdf_path):
    #formateo la URL para lidiar con los espacios
    titulo = urllib.parse.quote(pdf_path.split('/')[-1])
    tail = '/'.join(pdf_path.split('/')[:-1])
    path = tail + '/' + titulo

    #Para el caso especial de la Ñ
    if path.split('/')[-2] == 'Ñ':
        separado = path.split('/')
        separado[-2] = urllib.parse.quote(path.split('/')[-2])
        path = '/'.join(separado)
    #Descargo el archivo y creo un archivo nuevo donde guardarlo
    response = urllib.request.urlopen(path)
    file = open('pdfs_descargados/' + pdf_path.split('/')[-1], 'wb')
    file.write(response.read())
    file.close()
    return
print('Descargando archivos...')
for link in tqdm.tqdm(links[130:]):
    #import pdb; pdb.set_trace()
    descargar_pdf(link)



