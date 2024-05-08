import discord
import os
import re
from ..helpers import *

@discord.app_commands.command(name="news_experimental", description="Get the latest news for your class.")
async def news(ctx : discord.Interaction):
    s = GuildSettings(ctx.guild)

    if s.get("beta_programm") != True:
        await ctx.response.send_message(embed=simple_embed('Error', "Experimental Features are not activated."))
        return
    
    if check_if_class_is_set(ctx.guild) == False:
        await ctx.response.send_message(embed=simple_embed('Error', 'Class is not set.\n Set it with `/set class <classname>`'))

    parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(ctx.guild).get_file_name()}.pdf')

    msg = ''

    for class_name, events in parsed_plan.items():
        if s.get("class") in class_name:
            for event in events:
                msg += f"Am {event['date']} {event['day']} Stunde: {event["position"]}\n{event["cut_info"]}\n\n"

    if msg != '':
        await ctx.response.send_message(embed=simple_embed('News', f"```txt\n{msg}\n```"))
    else:
        await ctx.response.send_message(embed=simple_embed('Heute', 'Keine Neuigkeiten'))
