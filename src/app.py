import asyncio
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from enviorment.team.my_team import MY_TEAM
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer, MaxBasePowerPlayer
from poke_env import AccountConfiguration


async def main():
    bot1 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot2 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")

    #bot1 = RandomPlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    #bot2 = RandomPlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    print("Iniciando entrenamiento...")
    await bot1.battle_against(bot2, n_battles=100)
    print(f"Victorias bot1: {bot1.n_won_battles} de 100")
    #print(f"Epsilon: {bot1.agent.epsilon:.3f}")

asyncio.run(main())