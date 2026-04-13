import asyncio
from bots.first_bot.first_bot import FirstMovePlayer
from enviorment.team.my_team import MY_TEAM

async def main():
    bot1 = FirstMovePlayer(team=MY_TEAM, battle_format="gen9championsvgc2026regma")

    await bot1.send_challenges("Ardilla45", n_challenges=1)

asyncio.run(main())