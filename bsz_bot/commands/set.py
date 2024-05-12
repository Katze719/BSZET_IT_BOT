from typing import List
import discord
from ..helpers import *

async def autocomplete(
    ctx: discord.Interaction,
    current: str,
) -> List[discord.app_commands.Choice[str]]:
    settings = list(GuildSettings(ctx.guild).get_all_settings().keys())
    return [
        discord.app_commands.Choice(name=setting, value=setting)
        for setting in settings if current.lower() in setting.lower()
    ]

@discord.app_commands.command(name="set", description="Set a variable.")
@discord.app_commands.autocomplete(variable_name=autocomplete)
@admin_required
async def set(ctx : discord.Interaction, variable_name: str, value: str):
    """
    Set a variable.

    Args:
        ctx (discord.Interaction): The interaction context.
        variable_name (str): The name of the variable.
        value (str): The value to set the variable to.

    Returns:
        None
    """
    s = GuildSettings(ctx.guild)
    if variable_name in s.get_all_settings():
        if variable_name == 'output_name':
            await ctx.response.send_message(embed=simple_embed(f'Set {variable_name}', f"{variable_name} MARKED AS CAN NOT BE SET! (use sudo)"), ephemeral=True)
            return

        s.set(variable_name, value)
        if variable_name == 'routine' and (value == 'True' or value == 'true'):
            s.set('routine', 'True')
            s.set('routine_channel_id', ctx.channel.id)
            await ctx.response.send_message(embed=simple_embed(f'Set {variable_name} and routine_channel_id', f"{variable_name} was set to {value} and routine_channel_id was set to {ctx.channel.id}"), ephemeral=True)
            return
        await ctx.response.send_message(embed=simple_embed(f'Set {variable_name}', f"{variable_name} was set to {value}"), ephemeral=True)
        return
    await ctx.response.send_message(embed=simple_embed(f'Set {variable_name}', f"{variable_name} Does not exist!"), ephemeral=True)
