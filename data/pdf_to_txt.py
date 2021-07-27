#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 18:13:11 2021

@author: gmarzik
"""

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import os
from pathlib import Path

def convert_pdf_to_string(file_path):
    """
    Toma el path a un archivo .pdf, convierte el contenido a texto y lo guarda en una variable.
    Parameters
    ----------
    file_path : string
        Path que indica la ubicación del archivo .pdf a transformar,

    Returns
    -------
    txt : string
        Contenido de texto del archivo transformado.
    """
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)
    txt = output_string.getvalue()     
    return txt

def txt_correction(txt):
    """
    Toma una variable con el texto crudo y la edita para que queden únicamente las estrofas, separadas por un salto de línea.

    Parameters
    ----------
    txt : string
        Variable con el contenido del archivo de texto crudo.

    Returns
    -------
    txt_corr : string
        Variable con el contenido del archivo de texto adaptado al dataset.

    """
    lines = txt.split('\n')
    lines_corr = []
    for i in range(len(lines)):
        if lines[i] == 'ESTRIBILLO':
            continue
        if sum(1 for char in lines[i] if char.isupper()) > 1:
            continue
        if not lines[i] or not lines[i].strip():
            continue
        if '//' in  lines[i]:
            continue
        lines_corr.append(lines[i])
        if '.' in lines[i]:
            lines_corr.append('\n')
    return lines_corr

path_pdfs = '/media/gmarzik/Samsung_T5/RNN_chamame/chama-learn/data/pdfs_descargados'
path_txts = '/media/gmarzik/Samsung_T5/RNN_chamame/chama-learn/data/txts'        
nombre_archivos = [os.path.splitext(filename)[0] for filename in os.listdir(path_pdfs)]
num_archivos = len(nombre_archivos)

for i in range(num_archivos):
    text = convert_pdf_to_string(path_pdfs + '/' + nombre_archivos[i] + '.pdf')
    text_corr = txt_correction(text)
    file=open(path_txts + '/' +  nombre_archivos[i] + '.txt','w')
    join_txt='\n'.join(text_corr)
    file.write(join_txt)
    file.close()

