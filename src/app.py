import asyncio
import csv
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from enviorment.team.my_team import MY_TEAM
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer, MaxBasePowerPlayer

TOTAL_BATTLES = 100
VALIDATE_EVERY = 20
VALIDATION_BATTLES = 50


async def main():
    bot1 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot2 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    validator = SimpleHeuristicsPlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")

    with open("resultados/metricas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["batalla", "winrate_vs_heuristics", "epsilon"])

    print("Iniciando entrenamiento...")

    for i in range(0, TOTAL_BATTLES, VALIDATE_EVERY):

        batalla_actual = i // VALIDATE_EVERY + 1

        await bot1.battle_against(bot2, n_battles=VALIDATE_EVERY)

        bot1.agent.save(f"checkpoints/model_{batalla_actual}.keras")

        wins_before = bot1.n_won_battles
        await bot1.battle_against(validator, n_battles=VALIDATION_BATTLES)
        wins_vs_heuristics = bot1.n_won_battles - wins_before
        winrate = wins_vs_heuristics / VALIDATION_BATTLES * 100

        print(f"Batalla {batalla_actual} | Winrate vs Heuristics: {winrate:.1f}% | Epsilon: {bot1.agent.epsilon:.3f}")

        with open("resultados/metricas.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([batalla_actual, winrate, bot1.agent.epsilon])


asyncio.run(main())