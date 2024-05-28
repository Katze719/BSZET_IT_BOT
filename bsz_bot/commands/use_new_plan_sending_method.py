import discord
from ..helpers import *

@discord.app_commands.command(name="use_new_plan_sending_method", description="Use the new plan sending method.")
@admin_required
@needs_class
async def use_new_plan_sending_method(ctx : discord.Interaction):
    GuildSettings(ctx.guild).set("use_old_plan_function", False)
    await ctx.response.send_message(embed=simple_embed(f'Using new plan sending method!'))
