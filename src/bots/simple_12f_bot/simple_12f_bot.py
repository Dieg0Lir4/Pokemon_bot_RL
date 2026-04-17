import numpy as np
from poke_env.player import RandomPlayer
from poke_env.battle import DoubleBattle
from poke_env.player.battle_order import DoubleBattleOrder
from enviorment.battle.battle import get_features, get_reward, get_active_pokemons
from models.dnn.dnn_build import predict_action

class Simple12fBot(RandomPlayer):
    def choose_move(self, battle):
        try:
            features = get_features(battle)
            q_values =predict_action(features)
            action = np.argmax(q_values)
            print("Chosen action:", action)
            new_action = self.action_to_order(q_values=q_values, battle=battle)
            return new_action
        except Exception as e:
            print(f"Error eligiendo acción: {e}")
            return self.choose_random_move(battle)
    
    def action_to_order(self, q_values: int, battle: DoubleBattle):
        print("Converting action to order:", q_values)
        action_for_p1 = np.argmax(q_values[:8])
        action_for_p2 = np.argmax(q_values[8:])
        own = get_active_pokemons(battle=battle)
        print("Own", own)
        print()
        print()
        print("own[0].moves", type(own[0].moves))
        print()
        print("own[0].moveskeys", type(list(own[0].moves)))
        print("own[0] move", list(own[0].moves)[0])
        print("own[1] move", list(own[1].moves)[0])
        return DoubleBattleOrder(
            first_order=self.create_order(own[0].moves[list(own[0].moves)[0]]) if own[0] else None,
            second_order=self.create_order(own[1].moves[list(own[1].moves)[0]]) if own[1] else None
        )
        