import discord
from ..helpers import *

@discord.app_commands.command(name="activate_experimental_features", description="Activates the Experimental Features")
async def activate_beta_features(ctx : discord.Interaction):
    """
    Activates the bot.

    Args:
        ctx (discord.Interaction): The interaction context.

    Returns:
        None
    """
    if check_if_class_is_set(ctx.guild) == False:
        await ctx.response.send_message(embed=simple_embed('Error', 'Class is not set.\n Set it with `/set class <classname>`'))
        return
    GuildSettings(ctx.guild).set("beta_programm", True)
    await ctx.response.send_message(embed=simple_embed(f'Activated Experimental Features!'))
