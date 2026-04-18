from collections import deque
from models.dqn.dqn_model import build_model, predict_action
import random
import numpy as np
import tensorflow as tf

class DQNAgent:
    def __init__(self):
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 64

        self.memory = deque(maxlen=10000)
        self.model = build_model()
        self.target_model = build_model()
        self.target_model.set_weights(self.model.get_weights())

    def act(self, state: np.ndarray) -> int:
        if np.random.rand() <= self.epsilon:
            return random.randrange(8), random.randrange(8)
        q_values = predict_action(self.model, state)
        action_p1 = int(np.argmax(q_values[:8]))
        action_p2 = int(np.argmax(q_values[8:]))

        return action_p1, action_p2
    
    def remember(self, state, action_p1, action_p2, reward, next_state, done):
       self.memory.append((state, action_p1, action_p2, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            print(f"Buffer insuficiente: {len(self.memory)}/{self.batch_size}")
            return
        
        minibatch = random.sample(self.memory, self.batch_size)

        states      = np.array([s for s, *_ in minibatch])
        actions_p1  = np.array([a1 for _, a1, *_ in minibatch])
        actions_p2  = np.array([a2 for _, _, a2, *_ in minibatch])
        rewards     = np.array([r for _, _, _, r, *_ in minibatch])
        next_states = np.array([ns for _, _, _, _, ns, _ in minibatch])
        dones       = np.array([d for *_, d in minibatch])

        q_values = self.model.predict(states, verbose=0)
        next_values = self.target_model.predict(next_states, verbose=0)

        target_p1 = rewards + self.gamma * np.max(next_values[:, :8], axis=1) * (1 - dones)
        target_p2 = rewards + self.gamma * np.max(next_values[:, 8:], axis=1) * (1 - dones)

        q_values[np.arange(self.batch_size), actions_p1] = target_p1
        q_values[np.arange(self.batch_size), actions_p2 + 8] = target_p2

        self.model.fit(states, q_values, epochs=1, verbose=0)
        print(f"Modelo actualizado | epsilon: {self.epsilon:.3f}")


        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save(self, path: str):
        self.model.save(path)

    def load(self, path: str):
        self.model = tf.keras.models.load_model(path)
        self.target_model.set_weights(self.model.get_weights())