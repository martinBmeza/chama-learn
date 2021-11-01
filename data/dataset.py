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
    [encoded_dataset] = np.array(tokenizer.texts_to_sequences([chamame_text]))-1
    max_caracteres = len(tokenizer.word_index)
    return encoded_dataset, max_caracteres, tokenizer


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


def window_sequence(dataset,n_steps,batch_size,max_carac,buffer_size,shift=1,shuffle=True):
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
    shift: int
        Cantidad de caracteres entre ventanas. 1 (default) para statless RNN (las ventanas avanzan de a 1 caracter), n_steps para stateful RNN (avanzan de a ventanas)    
    shuffle: bool
        Mezclar o no los tensores que contienen las ventanas de caracteres. Default true (stateless).
    
    Returns
    -------
    dataset_final : PrefetchDataset
        Conjunto de datos procesado.

    """
    window_length = n_steps + 1 #se busca predecir el próximo caracter
    dataset_windowed = dataset.window(window_length,shift=shift,drop_remainder=True) #dividimos la secuencia en sub-secuencias de window_length caracteres
    dataset_tensors = dataset_windowed.flat_map(lambda window: window.batch(window_length)) #convertimos de dataset de sub datasets a dataset de tensores
    #El shuffle es solo para Statless, en stateful buscamos ventanas consecutivas (por eso los batch de 1 también)
    if (shuffle):
        dataset_shuf = dataset_tensors.shuffle(1000000).batch(batch_size) #desordenamos los tensores
    else:
        dataset_shuf = dataset_tensors.copy()
        dataset_shuf = dataset_shuf.batch(1)
    dataset_armado = dataset_shuf.map(lambda windows: (windows[:,:-1],windows[:,1:])) #se separan los inputs (primeros n_steps caracteres) de los outputs (úlitmo caracter)
    dataset_one_hot_encoded = dataset_armado.map(lambda X_batch, Y_batch: (tf.one_hot(X_batch,depth=max_carac), Y_batch)) #se codifica usando one hot vectors para tener ceros o unos de input nada más (chequear si max_carac no es muy alto)
    dataset_final = dataset_one_hot_encoded.prefetch(buffer_size) #se agrega el prefetch para tener listas nuevas instancias mientras se procesa la instancia actual
    return dataset_final

<<<<<<< HEAD

if __name__ == '__main__':
    a,b = dataset_pre('/txts/chamame_dataset.txt')

    c,d = dataset_split(a,90)

    e = window_sequence(c,100,32,b,1)

    for element in e:
        print(element[0])
        #print(element[1])#primero los inputs one hot encodeados y después los outputs como enteros normales
=======
# e = window_sequence(c,100,32,b,1)

# for element in e:
#     print(element[0])
    #print(element[1])#primero los inputs one hot encodeados y después los outputs como enteros normales
    
#Para stateful RNN
def batch_stateful(encoded_dataset,train_s,batch_size,n_steps,max_carac):
    """
    Armado de dataset para trabajar con batches distintos de 1 en stateful RNN

    Parameters
    ----------
    encoded_dataset : ndarray
        Conjunto de datos.
    train_size : int
        Porcentaje del conjunto de datos destinado al entrenamiento.
    batch_size : int
        Número de divisiones del conjunto de datos.
    n_steps : int
        Salto entre ventanas (máxima longitud de la cadena de caracteres que la red puede aprender).
    max_carac : int
        Cantidad de caracteres distintos del modelo.

    Returns
    -------
    dataset : PrefetchDataset
        Conjunto de datos procesado.

    """
    train_size = train_s * len(encoded_dataset) // 100
    window_length = n_steps + 1 #se busca predecir 1 caracter para adelante
    #divido el array que contiene al dataset codificado en batch_size partes iguales
    encoded_parts = np.array_split(encoded_dataset[:train_size], batch_size)
    datasets = []
    #genero 32 datasets de tensores, cada uno con ventanas consecutivas
    for encoded_part in encoded_parts:
        dataset = tf.data.Dataset.from_tensor_slices(encoded_part)
        dataset = dataset.window(window_length, shift=n_steps, drop_remainder=True)
        dataset = dataset.flat_map(lambda window: window.batch(window_length))
        datasets.append(dataset)
    #uno los batch_size datasets en uno solo, manteniendo la condición de consecutividad entre las ventanas     
    dataset_global = tf.data.Dataset.zip(tuple(datasets)).map(lambda *windows: tf.stack(windows))
    dataset = dataset_global.map(lambda windows: (windows[:, :-1], windows[:, 1:]))
    dataset = dataset.map(lambda X_batch, Y_batch: (tf.one_hot(X_batch, depth=max_carac), Y_batch))
    dataset = dataset.prefetch(1)
    return dataset

# f = batch_stateful(a,90,128,100,b)

# for element in f:
#     print(element[0])




    
>>>>>>> a14fb6abb21aa681a150696da505362988ba8a4c

    
