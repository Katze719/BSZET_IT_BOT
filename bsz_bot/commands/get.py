from typing import List
import discord
from ..helpers import *

async def autocomplete(
    ctx: discord.Interaction,
    current: str,
) -> List[discord.app_commands.Choice[str]]:
    settings = list(GuildSettings(ctx.guild).get_all_settings().keys())
    settings.append('all')
    return [
        discord.app_commands.Choice(name=setting, value=setting)
        for setting in settings if current.lower() in setting.lower()
    ]

@discord.app_commands.command(name="get", description="Get a variable.")
@discord.app_commands.autocomplete(variable_name=autocomplete)
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
        await ctx.response.send_message(embed=simple_embed('All vars', response), ephemeral=True)
        return
    value = s.get(variable_name)
    await ctx.response.send_message(embed=simple_embed(f'Get {variable_name}',f"{variable_name} : {value}"), ephemeral=True)
