import discord
from ..helpers import *

@discord.app_commands.command(name="status", description="Get the bot status.")
async def status(ctx : discord.Interaction):
    s = GuildSettings(ctx.guild)
    beta_features = "Experimental Features: Active" if s.get("beta_programm") == True else "Experimental Features: Inactive"
    if s.get("routine") == True and s.get("routine_channel_id") != 0:
        
        
        await ctx.response.send_message(embed=simple_embed(f'Status: Active', f"The bot is currently active.\n{beta_features}\nRoutine Channel: {s.get("routine_channel_id")}\nClass: {s.get("class")}"))
    else:
        await ctx.response.send_message(embed=simple_embed(f'Status: Inactive', f"The bot is currently inactive.\n{beta_features}\nRoutine Channel: {s.get("routine_channel_id")}\nClass: {s.get("class")}"))
