import discord
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import tasks
from datetime import datetime, timedelta
from ..core import BSZ_BOT
from ..helpers import *

scheduler = AsyncIOScheduler()

async def get_news(id, time):
    logger.info("sending hourly news")

    for guild in BSZ_BOT.guilds:
        s = GuildSettings(guild)

        if s.get("beta_programm") != True:
            continue

        if s.get("routine") != True:
            continue

        parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(guild).get_file_name()}.pdf')

        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            continue

        msg = ''

        for event in parsed_plan:
            if s.get("class") in event["class"]:
                if is_today(event["date"]) and event["position"] == id:
                    msg += f"Lehrer: {event['teacher']}\nFach:   {event['subject']}\nRaum:   {event['room']}\nInfo:   {event['info']}\n\n"

        if msg != '':
            await channel.send(embed=simple_embed(f'Jetzt!', f"```txt\n{msg}\n```"))
        else:
            await channel.send(embed=simple_embed(f'Jetzt!', 'Keine Neuigkeiten'))

times_with_ids = {
    "7:10": 1,
    "9:10": 3,
    "10:55": 5,
    "13:05": 7
}

# Füge die Jobs für die angegebenen Zeiten hinzu
for time, id in times_with_ids.items():
    hour, minute = map(int, time.split(':'))
    scheduler.add_job(get_news, CronTrigger(hour=hour, minute=minute, day_of_week='mon-fri'), args=[id, time])
