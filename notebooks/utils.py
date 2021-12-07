import numpy as np
import tensorflow as tf

def generate_time_series(batch_size, n_steps):
    ''' Genera series de una sola variable. Suma 2 senos de diferente amplitud
    y fase, mas ruido.'''
    # [baches, time_steps]
    freq1, freq2, offsets1, offsets2 = np.random.rand(4, batch_size, 1) #en columnas
    time = np.linspace(0, 1, n_steps)
    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10)) # wave 1
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20)) # + wave 2
    series += 0.1 * (np.random.rand(batch_size, n_steps) - 0.5) # + noise entre -0.5 y + 0.5
    return series[..., np.newaxis].astype(np.float32) # nuevo eje para... 



class LNSimpleRNNCell(tf.keras.layers.Layer):
    def __init__(self, units, activation="tanh", **kwargs):
        super().__init__(**kwargs)
        self.state_size = units
        self.output_size = units
        self.simple_rnn_cell = tf.keras.layers.SimpleRNNCell(units, activation=None)
        self.layer_norm = tf.keras.layers.LayerNormalization()
        self.activation = tf.keras.activations.get(activation)
    
    def call(self, inputs, states):
        outputs, new_states = self.simple_rnn_cell(inputs, states)
        norm_outputs = self.activation(self.layer_norm(outputs))
        return norm_outputs, [norm_outputs]