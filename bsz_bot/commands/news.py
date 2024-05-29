import discord
import os
from ..helpers import *

@discord.app_commands.command(name="news", description="Get the latest news for your class.")
@needs_class
async def news(ctx : discord.Interaction):
    parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(ctx.guild).get_file_name()}.pdf')

    msg = ''

    for event in parsed_plan:
        if GuildSettings(ctx.guild).get("class").replace(" ", "").lower() in event["class"].replace(" ", "").lower():
            msg += f"```txt\nAm {event['date']} {event['day']}\nStunde: {event["hours"]}\nLehrer: {event["teacher"]}\nFach:   {event["subject"]}\nRaum:   {event["room"]}\nInfo:   {event["info"]}\n```\n"

    if msg != '':
        await ctx.response.send_message(embed=simple_embed('News', f"{msg}"))
    else:
        await ctx.response.send_message(embed=simple_embed('News', 'Keine Neuigkeiten'))
