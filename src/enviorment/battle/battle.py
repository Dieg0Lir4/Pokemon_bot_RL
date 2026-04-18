import numpy as np
from poke_env.battle import DoubleBattle


def get_features(battle: DoubleBattle) -> np.ndarray:

    own = get_active_pokemons(battle=battle)
    hp_own_1 = own[0].current_hp_fraction if own[0] else 0.0
    hp_own_2 = own[1].current_hp_fraction if own[1] else 0.0

    opp = battle.opponent_active_pokemon
    hp_opp_1 = opp[0].current_hp_fraction if opp[0] else 0.0
    hp_opp_2 = opp[1].current_hp_fraction if opp[1] else 0.0

    moves_p1 = own[0].moves
    moves_p2 = own[1].moves

    if not moves_p1:
        move_vector_p1 = np.zeros(4)
    else:
        move_vector_p1 = get_vector_of_moves(battle.available_moves[0], moves_p1) if own[0] else np.zeros(4)

    if not moves_p2:
        move_vector_p2 = np.zeros(4)
    else:
        move_vector_p2 = get_vector_of_moves(battle.available_moves[1], moves_p2) if own[1] else np.zeros(4)


    m1_p1, m2_p1, m3_p1, m4_p1 = move_vector_p1
    m1_p2, m2_p2, m3_p2, m4_p2 = move_vector_p2

    return np.array([
        hp_own_1, hp_own_2,
        hp_opp_1, hp_opp_2,
        m1_p1, m2_p1, m3_p1, m4_p1,
        m1_p2, m2_p2, m3_p2, m4_p2,
    ])

def get_reward(battle: DoubleBattle) -> float:
    if battle.won:
        return 1.0
    elif battle.lost:
        return -1.0
    return 0.0

def get_vector_of_moves(available_moves: list, moveset: dict) -> np.ndarray:
    move_vector = np.zeros(4)
    for i, move in enumerate(moveset.values()):
        if move in available_moves:
            move_vector[i] = 1.0
    return move_vector

def get_active_pokemons(battle: DoubleBattle) -> list:
    own = battle.active_pokemon
    p1 = own[0]
    p2 = own[1]
    return [p1, p2] 