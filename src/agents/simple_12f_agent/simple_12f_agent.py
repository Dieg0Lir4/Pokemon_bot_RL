from collections import deque
from models.dqn.dqn_model import build_model, predict_action
import random
import numpy as np

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
            return random.randrange(16)
        q_values = predict_action(self.model, state)
        return int(np.argmax(q_values))