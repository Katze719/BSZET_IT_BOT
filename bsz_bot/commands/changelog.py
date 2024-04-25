import discord
from ..helpers import *

@discord.app_commands.command(name="changelog", description="Gives you the last chengelog.")
async def changelog(ctx : discord.Interaction):
    await ctx.response.send_message(embed=simple_embed("Reset!", 'success'))
