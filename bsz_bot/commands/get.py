import discord
from ..helpers import *

@discord.app_commands.command(name="get", description="Get a variable.")
async def get(ctx : discord.Interaction, variable_name: str):
    s = GuildSettings(ctx.guild.id)
    if variable_name == 'all':
        response = "```toml\n"
        for key, value in s.get_all_settings().items():
            response += f"{key} : {value}\n"
        response += "```"
        await ctx.response.send_message(embed=simple_embed('All vars', response))
        return
    value = s.get(variable_name)
    await ctx.response.send_message(embed=simple_embed(f'Get {variable_name}',f"{variable_name} : {value}"))
