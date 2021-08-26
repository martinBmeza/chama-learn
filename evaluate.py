import tensorflow as tf
from tensorflow import keras
import numpy as np

def preprocess(texts, tokenizer):
    max_id = len(tokenizer.word_index) 
    X = np.array(tokenizer.texts_to_sequences(texts)) - 1
    return tf.one_hot(X, max_id)

def next_char(model, text, tokenizer, temperature=1):
    X_new = preprocess([text], tokenizer)
    y_proba = model.predict(X_new)[0, -1:, :]
    rescaled_logits = tf.math.log(y_proba) / temperature
    char_id = tf.random.categorical(rescaled_logits, num_samples=1) + 1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]

def complete_text(model, text, tokenizer, n_chars=50, temperature=1):
    for _ in range(n_chars):
        text += next_char(model, text, tokenizer, temperature)
    return text
