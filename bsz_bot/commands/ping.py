import discord
from ..helpers import *

@discord.app_commands.command(name="ping", description="Ping the bot to see if he reacts.")
async def ping(ctx : discord.Interaction):
    """
    Ping the bot to see if he reacts.

    Parameters:
        ctx (discord.Interaction): The interaction object representing the command invocation.

    Returns:
        None
    """
    await ctx.response.send_message(embed=simple_embed(f"Pong!"))
