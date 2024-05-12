import discord
import asyncio
import os
from discord.ext import tasks
from datetime import datetime, timedelta
from ..core import BSZ_BOT
from ..helpers import *

async def time_until(hour, minute):
    now = datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target_time:
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()

async def wait_until(hour, minute):
    wait_seconds = await time_until(hour, minute)
    await asyncio.sleep(wait_seconds)

@tasks.loop(hours=24)
async def get_news():
    logger.info("sending dayly info")

    if datetime.today().weekday() > 4:
        return

    for guild in BSZ_BOT.guilds:
        s = GuildSettings(guild)

        if s.get("beta_programm") != True:
            continue

        parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(guild).get_file_name()}.pdf')

        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            continue

        msg = ''

        for class_name, events in parsed_plan.items():
            if s.get("class") in class_name:
                for event in events:
                    if is_today(event["date"]):
                        msg += f"Stunde: {event["position"]}\n{event["cut_info"]}\n\n"

        if msg != '':
            await channel.send(embed=simple_embed('Heute', f"```txt\n{msg}\n```"))
        else:
            await channel.send(embed=simple_embed('Heute', 'Keine Neuigkeiten'))
            

@get_news.before_loop
async def before_daily_task():
    logger.info("waiting until 6:30")
    await wait_until(6, 30)