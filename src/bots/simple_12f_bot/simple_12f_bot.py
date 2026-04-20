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
        self.got_stuck_1 = False
        self.got_stuck_2 = False

    def choose_move(self, battle):
        try:
            state = get_features(battle)
            action = self.agent.act(state)

            if self.last_state is not None:
                reward = get_reward(battle)
                done = battle.finished
                self.agent.remember(
                    self.last_state,
                    self.last_action,
                    reward,
                    state,
                    done
                )
                self.agent.replay()
                
                if done:
                    if self.agent.epsilon > self.agent.epsilon_min:
                        self.agent.epsilon *= self.agent.epsilon_decay

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



    
    def attack(self, battle: DoubleBattle, input_action: int, pokemon_int: int):
        available_moves = battle.available_moves[pokemon_int]
        if not available_moves:
            return None
                
        opponent_active = battle.opponent_active_pokemon
        if not opponent_active:
            return None
        
        selected_index = random.choice(opponent_active)
        selected_target = opponent_active.index(selected_index) + 1

        selected_move = None
        move_index = input_action % len(available_moves)
        selected_move = available_moves[move_index]
        
        if selected_move is None:
            print(f"No se pudo seleccionar un movimiento para el Pokémon {pokemon_int} con input_action {input_action}")
            return None
        
        if selected_target is None:
            print(f"No se pudo seleccionar un objetivo para el Pokémon {pokemon_int} con input_action {input_action}")
            return None
        

        print("SKLJDFSLKÑDJF", selected_move)
        return self.create_order(selected_move);


