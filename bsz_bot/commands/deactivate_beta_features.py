import discord
from ..helpers import *

@discord.app_commands.command(name="deactivate_experimental_features", description="Deactivates the Experimental Features")
@admin_required
async def deactivate_beta_features(ctx : discord.Interaction):
    """
    Deactivates the beta features.

    Args:
        ctx (discord.Interaction): The interaction context.

    Returns:
        None
    """
    GuildSettings(ctx.guild).set("beta_programm", False)
    await ctx.response.send_message(embed=simple_embed(f'Deactivated Experimental Features!'))
