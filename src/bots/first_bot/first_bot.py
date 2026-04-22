from poke_env.player import RandomPlayer
from poke_env.battle import DoubleBattle
from poke_env.player.battle_order import DoubleBattleOrder

class FirstMovePlayer(RandomPlayer):
    def choose_move(self, battle):
        if isinstance(battle, DoubleBattle):
            orders = []
            for i in range(2):

                print("Moveset:", battle.active_pokemon[i].moves)
                print("Available moves:", battle.available_moves[i])

                moves = battle.available_moves[i] if i < len(battle.available_moves) else []
                switches = battle.available_switches[i] if i < len(battle.available_switches) else []

                if moves:
                    move = moves[0]
                    targets = battle.get_possible_showdown_targets(move, battle.active_pokemon[i])
                    target = targets[0] if targets else None
                    orders.append(self.create_order(move, move_target=target))
                elif switches:
                    orders.append(self.create_order(switches[0]))
                else:
                    orders.append(None)

            if orders[0] is None and orders[1] is None:
                return self.choose_random_move(battle)
            elif orders[0] is None:
                return orders[1]
            elif orders[1] is None:
                return orders[0]
            return DoubleBattleOrder(orders[0], orders[1])
        else:
            if battle.available_moves:
                return self.create_order(battle.available_moves[0])
            return self.choose_random_move(battle)
