import asyncio
import csv
from bots.simple_12f_bot.simple_12f_bot import Simple12fBot
from enviorment.team.my_team import MY_TEAM



async def main():
    bot1 = Simple12fBot(team=MY_TEAM, battle_format="gen9championsvgc2026regma")
    bot1.agent.load("checkpoints/model2/model2_155200.keras")

    await bot1.send_challenges("Ardilla45", n_challenges=1)


asyncio.run(main())