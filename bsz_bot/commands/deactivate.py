import discord
from ..helpers import *

@discord.app_commands.command(name="deactivate", description="Deactivates the bot")
@admin_required
async def deactivate(ctx : discord.Interaction):
    """
    Deactivates the bot.

    Args:
        ctx (discord.Interaction): The interaction context.

    Returns:
        None
    """
    GuildSettings(ctx.guild).set("routine", "False")
    await ctx.response.send_message(embed=simple_embed(f'Deactivated!', f"The bot will no longer inform you if a new substitution plan is available."))
