import numpy as np
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer
from poke_env.battle import DoubleBattle
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer, MaxBasePowerPlayer
from enviorment.battle.battle import get_features, get_reward
from agents.simple_12f_agent.simple_12f_agent import DQNAgent
import random

class Simple12fBot(RandomPlayer, SimpleHeuristicsPlayer, MaxBasePowerPlayer):
    def __init__(self, **kwargs):
        self.agent = DQNAgent()
        self.last_state = None
        self.last_action = None
        super().__init__(**kwargs)

    def choose_move(self, battle):
        try:
            self.battle_finised = battle
            state = get_features(battle)
            action = self.agent.act(state)

            if self.last_state is not None:
                reward = 0
                done = 0
                self.agent.remember(
                    self.last_state,
                    self.last_action,
                    reward,
                    state,
                    done
                )
                
            self.last_state = state
            self.last_action = action

            return self.action_to_order(action=action, battle=battle)
        except Exception as e:
            print("ERROR REAL:")
            raise e
        
    def action_to_order(self, action: int, battle: DoubleBattle):

        if action == 0:
            return RandomPlayer.choose_move(self, battle)
        elif action == 1:
            return MaxBasePowerPlayer.choose_move(self, battle)
        elif action == 2:
            return SimpleHeuristicsPlayer.choose_move(self, battle)
        else:
            print(f"Invalid action: {action}. Defaulting to random move.")
            return self.choose_random_doubles_move(battle)



