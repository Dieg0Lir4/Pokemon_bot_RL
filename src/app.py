import asyncio
import csv
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from enviorment.team.my_team import MY_TEAM
from poke_env.player import SimpleHeuristicsPlayer

TOTAL_BATTLES = 100
VALIDATE_EVERY = 20
VALIDATION_BATTLES = 5

async def main():
    bot1 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot2 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    validator = SimpleHeuristicsPlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")

    with open("resultados/metricas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["batalla", "winrate_vs_heuristics", "epsilon"])

    print("Iniciando entrenamiento...")

    wins_before = 0

    for i in range(TOTAL_BATTLES):
        try:
            await bot1.battle_against(bot2, n_battles=1)

            won = bot1.n_won_battles > wins_before
            wins_before = bot1.n_won_battles
            reward = 1.0 if won else -1.0

            if bot1.agent.memory:
                state, action, _, next_state, done = bot1.agent.memory[-1]
                bot1.agent.memory[-1] = (state, action, reward, next_state, 1)

            bot1.agent.replay()

            if (i + 1) % VALIDATE_EVERY == 0:
                batalla_actual = i + 1
                bot1.agent.save(f"checkpoints/model2/model2_{batalla_actual}.keras")

                wins_val_before = bot1.n_won_battles
                await bot1.battle_against(validator, n_battles=VALIDATION_BATTLES)
                wins_vs_heuristics = bot1.n_won_battles - wins_val_before
                winrate = wins_vs_heuristics / VALIDATION_BATTLES * 100

                print(f"Batalla {batalla_actual} | Winrate: {winrate:.1f}% | Epsilon: {bot1.agent.epsilon:.3f}")

                with open("resultados/metricas.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([batalla_actual, winrate, bot1.agent.epsilon])
        except Exception as e:
            print(f"Error en batalla {i}: {e}")
            continue

asyncio.run(main())