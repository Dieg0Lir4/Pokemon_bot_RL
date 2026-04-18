import numpy as np
from poke_env.player import RandomPlayer
from poke_env.battle import DoubleBattle
from poke_env.player.battle_order import DoubleBattleOrder
from enviorment.battle.battle import get_features, get_reward
from agents.simple_12f_agent.simple_12f_agent import DQNAgent

class Simple12fBot(RandomPlayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent = DQNAgent()
        self.last_state = None
        self.last_action_p1 = None
        self.last_action_p2 = None

    def choose_move(self, battle):
        try:
            state = get_features(battle)
            action_p1, action_p2 = self.agent.act(state)

            if self.last_state is not None:
                reward = get_reward(battle)
                done = battle.finished
                self.agent.remember(
                    self.last_state,
                    self.last_action_p1,
                    self.last_action_p2,
                    reward,
                    state,
                    done
                )
                self.agent.replay()

            self.last_state = state
            self.last_action_p1 = action_p1
            self.last_action_p2 = action_p2

            return self.action_to_order(action_p1, action_p2, battle)
        except Exception as e:
            print(f"Error: {e}")
            return self.choose_random_move(battle)
        
    def action_to_order(self, action_p1: int, action_p2: int, battle: DoubleBattle):
        return self.choose_random_move(battle)
        order_p2 = self.choose_random_move(battle)

        return DoubleBattleOrder(
            first_order=order_p1,
            second_order=order_p2
        )
    
    def get_valid_moves(self, battle: DoubleBattle, input_action: int, pokemon_int: int):
        available_moves = battle.available_moves[pokemon_int]
        if input_action < len(available_moves):
            return available_moves[input_action]
        else:
            return None