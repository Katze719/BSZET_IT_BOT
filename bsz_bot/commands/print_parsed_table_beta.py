import discord
import os
from ..helpers import *

@discord.app_commands.command(name="print_parsed_table_experimental", description="print the parsed table")
async def print_parsed_table_beta(ctx : discord.Interaction):
    parsed_dict = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{GuildSettings(ctx.guild).get("output_name")}.pdf')
            
    msg = ''
    for event in parsed_dict:
        msg += str(event) + '\n'

    await ctx.response.send_message(embed=simple_embed('Print Parsed Table', msg))
