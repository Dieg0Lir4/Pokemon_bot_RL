import numpy as np
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.Input(shape=(12,)),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dense(16, activation="linear")
])

def build_model():
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(12,)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(16, activation="linear")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="mse"
    )
    return model

def predict_action(features: np.ndarray) -> np.ndarray:
    print("feature shape:", features.shape)
    q_values = model(features.reshape(1, -1), training=False).numpy()
    return q_values[0]

