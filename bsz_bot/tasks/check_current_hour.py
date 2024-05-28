import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ..core import BSZ_BOT
from ..helpers import *

scheduler = AsyncIOScheduler()

async def get_news(id):
    logger.info("sending hourly news")

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
            if s.get("class") in event["class"]:
                if is_today(event["date"]) and f"{event["position"]}" == f"{id}":
                    msg += f"Stunde: {event['hours']}\nLehrer: {event['teacher']}\nFach:   {event['subject']}\nRaum:   {event['room']}\nInfo:   {event['info']}\n\n"

        if msg != '':
            await channel.send(embed=simple_embed(f'Nächste Stunde!', f"```txt\n{msg}\n```"))

times_with_ids = {
    "7:00": 1,
    "8:45": 3,
    "10:45": 5,
    "12:30": 7
}

# Füge die Jobs für die angegebenen Zeiten hinzu
for time, id in times_with_ids.items():
    hour, minute = map(int, time.split(':'))
    scheduler.add_job(get_news, CronTrigger(hour=hour, minute=minute, day_of_week='mon-fri'), args=[id])