from collections import deque
from models.dqn.dqn_model import build_model, predict_action
import random
import numpy as np
import tensorflow as tf

class DQNAgent:
    def __init__(self):
        self.gamma = 0.9999
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9975
        self.batch_size = 64

        self.memory = deque(maxlen=10000)
        self.model = build_model()
        self.target_model = build_model()
        self.target_model.set_weights(self.model.get_weights())
        self.episode_memory = []

    def act(self, state: np.ndarray) -> int:
        if np.random.rand() <= self.epsilon:
            return random.randrange(3)
        q_values = predict_action(self.model, state)
        return int(np.argmax(q_values))
    
    def remember(self, state, action, reward, next_state, done):
       self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        last_battle = len(self.episode_memory)

        # agarre los ultimos turnos de la batalla actual para entrenar con ellos
        minibatch = self.memory[-last_battle:]

        self.episode_memory = []



        states      = np.array([s for s, *_ in minibatch])
        actions     = np.array([a for _, a, *_ in minibatch])
        rewards     = np.array([r for _, _, r, *_ in minibatch])
        next_states = np.array([ns for _, _, _, ns, _ in minibatch])
        dones       = np.array([d for *_, d in minibatch])

        q_values  = self.model.predict(states, verbose=0)
        next_q    = self.target_model.predict(next_states, verbose=0)
        target    = rewards + self.gamma * np.max(next_q, axis=1) * (1 - dones)

        q_values[np.arange(len(minibatch)), actions] = target

        self.model.fit(states, q_values, epochs=1, verbose=0)

        #if self.epsilon > self.epsilon_min:
            #self.epsilon *= self.epsilon_decay
    
    def save(self, path: str):
        self.model.save(path)

    def load(self, path: str):
        self.model = tf.keras.models.load_model(path)
        self.target_model.set_weights(self.model.get_weights())