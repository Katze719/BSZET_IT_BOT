import discord
from discord.ext import tasks
from ..core import BSZ_BOT
from ..helpers import *

@tasks.loop(seconds=30)
async def check_plan():
    plan = Plan()

    logger.info("checking for new plan")
    if not plan.new_plan_available():
        if plan.any_errors():
            logger.error("check_plan failed")
        return

    for guild in BSZ_BOT.guilds:
        s = GuildSettings(guild.id)
        if s.get("routine") != "True" or s.get("routine_channel_id") == None:
            continue
        file = discord.File(f"{plan.get_file_name()}.png")
        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if channel:
            await channel.send(file=file, embed=simple_embed('Neuer Vertretungsplan!', '', f"attachment://{plan.get_file_name()}.png"))
