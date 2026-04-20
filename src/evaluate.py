import asyncio
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from agents.simple_12f_agent.simple_12f_agent import DQNAgent
from enviorment.team.my_team import MY_TEAM

class EvaluationBot(Simple12fBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_log = []

    def choose_move(self, battle):
        try:
            from enviorment.battle.battle import get_features
            state = get_features(battle)
            action = self.agent.act(state)
            self.action_log.append(action)
            return self.action_to_order(action=action, battle=battle)
        except Exception as e:
            return self.choose_random_doubles_move(battle)

async def main():
    bot = EvaluationBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot.agent.load("checkpoints/model_25.keras")
    bot.agent.epsilon = 0.0

    opponent = SimpleHeuristicsPlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")

    await bot.battle_against(opponent, n_battles=100)


    counts = Counter(bot.action_log)
    labels = {0: "Random", 1: "MaxBasePower", 2: "SimpleHeuristics"}
    
    plt.figure(figsize=(8, 5))
    plt.bar([labels[k] for k in sorted(counts)], [counts[k] for k in sorted(counts)])
    plt.xlabel("Estrategia")
    plt.ylabel("Veces elegida")
    plt.title("Acciones elegidas en 100 batallas")
    plt.savefig("resultados/acciones.png")
    plt.show()
    print(f"Victorias: {bot.n_won_battles} de 100")

asyncio.run(main())