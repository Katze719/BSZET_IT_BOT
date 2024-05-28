import discord
from ..helpers import *

@discord.app_commands.command(name="plan", description="Get the plan.")
async def plan(ctx : discord.Interaction):
    """
    Get the plan and send it as a message to the Discord interaction.

    Parameters:
        ctx (discord.Interaction): The Discord interaction object.

    Returns:
        None
    """
    plan = Plan(ctx.guild)
    error_code = await plan.download()
    if error_code != 200:
        s = GuildSettings(ctx.guild)
        await ctx.response.send_message(embed=simple_embed(f"request: {error_code}", f"""ERROR: the pdf document could not be downloaded with:
                                                    `File URL: {s.get('file_url')}`
                                                    `Username: {s.get('username')}`
                                                    `Password: {s.get('password')}`
                                                    
                                                    The Bot will now stop sending messages until the error is fixed.
                                                    
                                                    Debugging tips:
                                                    
                                                    - use `/plan` from now on, since the Bot stoped sending messages
                                                    - try `/get all` to see all variables
                                                    - try changing the `file_url` with `/set file_url <new value>`
                                                    - try changing the `username` with `/set username <new value>`
                                                    - try changing the `password` with `/set password <new value>`
                                                    - if you want to change a value back to default, use\n`/set <variable> (use default)` or `/reset`\n
                                                    If that doesn't work, please open an issue on the GitHub repository.
                                                    https://github.com/Katze719/BSZET_IT_BOT
                                                    
                                                    """))
        return
    
    file = discord.File(f"{plan.get_file_name()}.png")
    await ctx.response.send_message(file=file, embed=simple_embed('Aktueller Vertretungsplan', '', f"attachment://{plan.get_file_name()}.png"))


