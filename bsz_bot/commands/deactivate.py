import discord
from ..helpers import *

@discord.app_commands.command(name="deactivate", description="Deactivates the bot")
async def deactivate(ctx : discord.Interaction):
    GuildSettings(ctx.guild.id).set("routine", "False")
    await ctx.response.send_message(embed=simple_embed(f'Deactivated!', f"The bot will no longer inform you if a new substitution plan is available."))
