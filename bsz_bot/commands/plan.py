import discord
from ..helpers import *

@discord.app_commands.command(name="plan", description="Get the plan.")
async def plan(ctx : discord.Interaction):
    plan = Plan()
    error_code = plan.download()
    if error_code != 200:
        await ctx.response.send_message(embed=simple_embed(f"request: {error_code}", "ERROR: the pdf document could not be downloaded (ask Paul D. for more Information)"))
        return
    file = discord.File(f"{plan.get_file_name()}.png")
    await ctx.response.send_message(file=file, embed=simple_embed('Aktueller Vertretungsplan', '', f"attachment://{plan.get_file_name()}.png"))


