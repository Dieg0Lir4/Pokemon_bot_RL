import numpy as np
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation="relu", input_shape=(12,))
    
])