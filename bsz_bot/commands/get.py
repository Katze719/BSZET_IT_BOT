import discord
from ..helpers import *

@discord.app_commands.command(name="get", description="Get a variable.")
async def get(ctx : discord.Interaction, variable_name: str):
    """
    Get a variable.

    Args:
        ctx (discord.Interaction): The interaction context.
        variable_name (str): The name of the variable.

    Returns:
        None
    """
    s = GuildSettings(ctx.guild)
    if variable_name == 'all':
        response = "```toml\n"
        for key, value in s.get_all_settings().items():
            response += f"{key} : {value}\n"
        response += "```"
        await ctx.response.send_message(embed=simple_embed('All vars', response))
        return
    value = s.get(variable_name)
    await ctx.response.send_message(embed=simple_embed(f'Get {variable_name}',f"{variable_name} : {value}"))
