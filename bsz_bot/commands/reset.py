import discord
from ..helpers import *

@discord.app_commands.command(name="reset", description="Reset the guild settings.")
@admin_required
async def reset(ctx : discord.Interaction):
    """
    Reset the guild settings.

    Parameters:
        ctx (discord.Interaction): The interaction object representing the command invocation.

    Returns:
        None
    """
    s = GuildSettings(ctx.guild)
    s.settings.clear()
    s.save_settings()
    await ctx.response.send_message(embed=simple_embed("Reset!", 'success'), ephemeral=True)
