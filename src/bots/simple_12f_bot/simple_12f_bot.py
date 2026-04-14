from poke_env.player import RandomPlayer
from poke_env.battle import DoubleBattle
from poke_env.player.battle_order import DoubleBattleOrder
from enviorment.battle.battle import get_features, get_reward

class Simple12fBot(RandomPlayer):
    def choose_move(self, battle):
        features = get_features(battle)

        
        