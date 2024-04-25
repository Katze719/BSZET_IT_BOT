import discord
from ..helpers import *

@discord.app_commands.command(name="reset", description="Reset the guild settings.")
async def reset(ctx : discord.Interaction):
    s = GuildSettings(ctx.guild.id)
    s.settings.clear()
    s.save_settings()
    await ctx.response.send_message(embed=simple_embed("Reset!", 'success'))
