import discord
from ..helpers import *

@discord.app_commands.command(name="set", description="Set a variable.")
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
    s = GuildSettings(ctx.guild.id)
    if variable_name in s.get_all_settings():
        s.set(variable_name, value)
        if variable_name == 'routine' and (value == 'True' or value == 'true'):
            s.set('routine', 'True')
            s.set('routine_channel_id', ctx.channel.id)
            await ctx.response.send_message(embed=simple_embed(f'Set {variable_name} and routine_channel_id', f"{variable_name} was set to {value} and routine_channel_id was set to {ctx.channel.id}"))
            return
        await ctx.response.send_message(embed=simple_embed(f'Set {variable_name}', f"{variable_name} was set to {value}"))
        return
    await ctx.response.send_message(embed=simple_embed(f'Set {variable_name}', f"{variable_name} Does not exist!"))
