#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 14:08:35 2021

@author: gmarzik
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np

def dataset_pre(path_file):
    """
    Codifica los caracteres de un archivo de texto que contiene todos los datos de entrenamiento a números enteros de 0 a 45. 

    Parameters
    ----------
    path_file : string.
        Path a la ubicación del archivo de texto que contiene el conjunto de datos.

    Returns
    -------
    encoded_dataset : ndarray
        Array que contiene los datos codificados.
    max_caracteres : int
        Número de caracteres distintos del dataset.
    """
    with open(path_file) as f:
        chamame_text = f.read()
    tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts(chamame_text)
    encoded_dataset = np.array(tokenizer.texts_to_sequences(chamame_text))-1
    max_caracteres = len(tokenizer.word_index)
    return encoded_dataset, max_caracteres

a,b = dataset_pre('/txts/chamame_dataset.txt')

def dataset_split(encoded_d,train_s):
    """
    Toma el conjunto de datos y lo divide en entrenamiento y validación.

    Parameters
    ----------
    encoded_d : ndarray
        Conjunto de datos.
    train_s : int
        Porcentaje del conjunto de datos destinado al entrenamiento.

    Returns
    -------
    train_set : TensorSliceDataset
        Conjunto de datos de entrenamiento.
    val_set : TensorSliceDataset
        Conjunto de datos de validación.

    """
    train_size = train_s * len(encoded_d) // 100
    train_set = tf.data.Dataset.from_tensor_slices(encoded_d[:train_size])
    val_set = tf.data.Dataset.from_tensor_slices(encoded_d[train_size:])
    return train_set,val_set

c,d = dataset_split(a,90)

def window_sequence(dataset,n_steps,batch_size,max_carac,buffer_size):
    """
    Se ventanea el conjunto de datos de entrenamiento para pasar de una única secuencia a muchas sub-secuencias. Se separa entre inputs y outputs del modelo. Se codifican las entradas para que sean 0's o 1's.
    

    Parameters
    ----------
    dataset : TensorSliceDataset
        Conjunto de datos a procesar.
    n_steps : int
        Salto entre ventanas (máxima longitud de la cadena de caracteres que la red puede aprender).
    batch_size : int
        Tamaño del batch para entrenamiento.
    max_carac : int
        Cantidad de caracteres distintos del modelo.
    buffer_size : int
        Cantidad de instancias de entrenamiento preparadas mientras se procesa la instancia actual.

    Returns
    -------
    dataset_final : PrefetchDataset
        Conjunto de datos procesado.

    """
    window_length = n_steps + 1 #se busca predecir el próximo caracter
    dataset_windowed = dataset.window(window_length,shift=1,drop_remainder=True) #dividimos la secuencia en sub-secuencias de window_length caracteres
    dataset_tensors = dataset_windowed.flat_map(lambda window: window.batch(window_length)) #convertimos de dataset de sub datasets a dataset de tensores
    dataset_shuf = dataset_tensors.shuffle(1000000).batch(batch_size) #desordenamos los tensores
    dataset_armado = dataset_shuf.map(lambda windows: (windows[:,:-1],windows[:,1:])) #se separan los inputs (primeros n_steps caracteres) de los outputs (úlitmo caracter)
    dataset_one_hot_encoded = dataset_armado.map(lambda X_batch, Y_batch: (tf.one_hot(X_batch,depth=max_carac), Y_batch)) #se codifica usando one hot vectors para tener ceros o unos de input nada más (chequear si max_carac no es muy alto)
    dataset_final = dataset_one_hot_encoded.prefetch(buffer_size) #se agrega el prefetch para tener listas nuevas instancias mientras se procesa la instancia actual
    return dataset_final

e = window_sequence(c,100,32,b,1)

for element in e:
    print(element[0])
    #print(element[1])#primero los inputs one hot encodeados y después los outputs como enteros normales

    
