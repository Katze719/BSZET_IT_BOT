import discord
from ..helpers import *

@discord.app_commands.command(name="use_old_plan_sending_method", description="Use the old plan sending method.")
@admin_required
async def use_old_plan_sending_method(ctx : discord.Interaction):
    GuildSettings(ctx.guild).set("use_old_plan_function", True)
    await ctx.response.send_message(embed=simple_embed(f'Using old plan sending method!'))
