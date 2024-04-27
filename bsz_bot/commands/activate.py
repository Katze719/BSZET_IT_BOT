import discord
from ..helpers import *

@discord.app_commands.command(name="activate", description="Activates the bot")
async def activate(ctx : discord.Interaction):
    """
    Activates the bot.

    Args:
        ctx (discord.Interaction): The interaction context.

    Returns:
        None
    """
    s = GuildSettings(ctx.guild.id)
    s.set("routine", "True")
    s.set("routine_channel_id", ctx.channel.id)
    await ctx.response.send_message(embed=simple_embed(f'Activated!', f"The bot will now inform you in this channel HERE ({ctx.channel.id}) if a new substitution plan is available."))
