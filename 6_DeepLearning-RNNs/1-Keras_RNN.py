'''
siehe Bilder in diesem Ordner

einmal eigene Implementierung und einmal Keras Implementierung
'''

import random

import numpy as np

import tensorflow as tf

from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.activations import *

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

class SimpleRNNInference:           # False: Many to One -> ein Output  True: Many to Many -> Output nach jeder "Berechnung"
    def __init__(self, rnn_layer, return_sequences=False):
        self.return_sequences = return_sequences
        self.rnn_layer = rnn_layer
        self.W, self.U, self.b = self.rnn_layer.get_weights() # Weight1-W Weight2-U Bias-b
        self.units = self.b.shape[0]

    # magic method call überschreiben
    def __call__(self, x):
        # output shape (num_timesteps, units)
        if self.return_sequences:
            self.time_steps = x.shape[0]
            self.h = np.zeros((self.time_steps, self.units))
        # output shape (units)
        else:
            self.h = np.zeros((self.units))
        h_t = np.zeros((1, self.units))
        for t, x_t in enumerate(x):
            x_t = x_t.reshape(1, -1) # (2) => (1, 2)
            h_t = self.forward_step(x_t, h_t)
            if self.return_sequences:
                self.h[t] = h_t
            else:
                self.h = h_t
        return self.h

    # Berechnung
    def forward_step(self, x_t, h_t):
        h_t = np.matmul(h_t, self.U) + np.matmul(x_t, self.W) + self.b
        h_t = tanh(h_t) # (-1, 1)
        return h_t
        

# data set shape = (num_samples, num_timesteps, num_features)
# input shape = (num_timesteps, num_features)
# If return_sequences == True:
# output shape = (num_timesteps, units)
# Else:
# output shape = (1, units)
x = np.random.normal(size=(1, 3, 2))
units = 4
return_sequences = True

# num_features = 2
# units = 4
# h_t shape = (4),        (units)       
# W shape   = (2, 4),     (num_features, units)
# U shape   = (4, 4),     (units, units)
# b shape   = (4),        (units)
# 
# matmul(x, W)      (1, 2)*(2,4) => (4)
# matmul(h, U)      (1, 4)*(4,4) => (4)
# intern + b        (4)+(4)   => (4) 

# Keras Implementation
model = Sequential()
model.add(SimpleRNN(units=units, return_sequences=return_sequences, input_shape=x.shape[1:]))
model.compile(loss="mse", optimizer="Adam")
#model.summary()

# Implementation without Keras
rnn = SimpleRNNInference(rnn_layer=model.layers[0], return_sequences=return_sequences)
output_rnn_own = rnn(x[0]) # 10.5 aufrufen der call Methode
print(output_rnn_own)
print("\n\n")
output_rnn_tf = model.predict(x[[0]])
print(output_rnn_tf) # 10.5
# überprüfen ob unsere eigene Implementierung korrekt ist 
assert np.all(np.isclose(output_rnn_own - output_rnn_tf, 0.0, atol=1e-06))