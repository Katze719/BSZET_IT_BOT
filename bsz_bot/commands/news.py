import discord
import os
from ..helpers import *

@discord.app_commands.command(name="news_experimental", description="Get the latest news for your class.")
@experimental
@needs_class
async def news(ctx : discord.Interaction):
    parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(ctx.guild).get_file_name()}.pdf')

    msg = ''

    for class_name, events in parsed_plan.items():
        if GuildSettings(ctx.guild).get("class") in class_name:
            for event in events:
                msg += f"Am {event['date']} {event['day']} Stunde: {event["position"]}\n{event["cut_info"]}\n\n"

    if msg != '':
        await ctx.response.send_message(embed=simple_embed('News', f"```txt\n{msg}\n```"))
    else:
        await ctx.response.send_message(embed=simple_embed('News', 'Keine Neuigkeiten'))
