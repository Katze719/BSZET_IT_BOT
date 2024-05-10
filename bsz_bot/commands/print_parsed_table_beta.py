import discord
import os
from ..helpers import *

@discord.app_commands.command(name="print_parsed_table_experimental", description="print the parsed table")
async def print_parsed_table_beta(ctx : discord.Interaction):
    parsed_dict = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{GuildSettings(ctx.guild).get("output_name")}.pdf')
    msg = ""
    
    for class_name, events in parsed_dict.items():
        msg += f"Class: {class_name}\n"
        for event in events:
            msg += f"{event["full_info"]}\n"
            pass
            
    await ctx.response.send_message(embed=simple_embed('Print Parsed Table', msg))
