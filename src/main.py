import asyncio
import csv
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from bots.multiple_bot.multiple_bot import MultipleBot
from enviorment.team.my_team import MY_TEAM
from poke_env.player import RandomPlayer, SimpleHeuristicsPlayer, MaxBasePowerPlayer


async def main():
    bot1 = MultipleBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot2 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    
    print("Iniciando batalla de prueba...")
    await bot1.battle_against(bot2, n_battles=1)

asyncio.run(main())