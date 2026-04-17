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

            print(f"Turno: {battle.turn}, Acción P1: {action_p1}, Acción P2: {action_p2}")

            return self.action_to_order(action_p1, action_p2, battle)
        except Exception as e:
            print(f"Error: {e}")
            return self.choose_random_move(battle)
        
    def action_to_order(self, action_p1: int, action_p2: int, battle: DoubleBattle):
        moves_p1 = battle.available_moves[0] if len(battle.available_moves) > 0 else []
        moves_p2 = battle.available_moves[1] if len(battle.available_moves) > 1 else []
        switches = battle.available_switches

        #Primr Pokemon
        if action_p1 <= 3 and action_p1 < len(moves_p1):
            order_p1 = self.create_order(moves_p1[action_p1])
        elif action_p1 <= 7:
            idx = action_p1 - 4
            order_p1 = self.create_order(switches[idx]) if idx < len(switches) else None
        else:
            order_p1 = None

        #Segundo Pokemon
        if action_p2 <= 3 and action_p2 < len(moves_p2):
            order_p2 = self.create_order(moves_p2[action_p2])
        elif action_p2 <= 7:
            idx = action_p2 - 4
            order_p2 = self.create_order(switches[idx]) if idx < len(switches) else None
        else:
            order_p2 = None

        if order_p1 is None or order_p2 is None:
            return self.choose_random_move(battle)

        return DoubleBattleOrder(
            first_order=order_p1,
            second_order=order_p2
        )