import discord
from ..helpers import *

@discord.app_commands.command(name="ping", description="Ping the bot to see if he reacts.")
async def ping(ctx : discord.Interaction):
    await ctx.response.send_message(embed=simple_embed(f"Pong!"))
