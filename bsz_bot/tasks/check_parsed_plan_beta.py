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
    
    if datetime.today().weekday() == 4 or datetime.today().weekday() == 5:
        return

    for guild in BSZ_BOT.guilds:
        s = GuildSettings(guild)

        if s.get("use_old_plan_function") == True:
            continue

        if s.get("routine") != True:
            continue

        await Plan(guild).download()
        parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(guild).get_file_name()}.pdf')

        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            continue

        msg = ''

        for event in parsed_plan:
            if s.get("class").replace(" ", "").lower() in event["class"].replace(" ", "").lower():
                if is_tomorrow(event["date"]):
                    msg += f"Stunde: {event["hours"]}\nLehrer: {event["teacher"]}\nFach:   {event["subject"]}\nRaum:   {event["room"]}\nInfo:   {event["info"]}\n\n"

        if msg != '':
            await channel.send(embed=simple_embed('Morgen', f"```txt\n{msg}\n```"))
            

@get_news.before_loop
async def before_daily_task():
    logger.info("waiting until 18:00")
    await wait_until(18, 00)