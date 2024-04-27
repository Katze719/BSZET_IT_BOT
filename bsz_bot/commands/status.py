import discord
from ..helpers import *

@discord.app_commands.command(name="status", description="Get the bot status.")
async def status(ctx : discord.Interaction):
    s = GuildSettings(ctx.guild)
    if s.get("routine") == "True" and s.get("routine_channel_id") != 0:
        await ctx.response.send_message(embed=simple_embed(f'Status: Active', "The bot is currently active."))
    else:
        await ctx.response.send_message(embed=simple_embed(f'Status: Inactive', "The bot is currently inactive."))
