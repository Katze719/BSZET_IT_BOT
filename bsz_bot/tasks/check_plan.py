import discord
from discord.ext import tasks
from ..core import BSZ_BOT
from ..helpers import *

@tasks.loop(minutes=5)
async def check_plan():
    """
    Asynchronous task that checks for a new plan every 5 minutes.

    This function is decorated with `@tasks.loop(minutes=5)` to run it every 5 minutes.
    It checks for a new plan by creating a `Plan` object and calling its `new_plan_available()` method.
    If no new plan is available, it checks if there are any errors by calling the `any_errors()` method of the `Plan` object.
    If there are errors, it logs an error message with the text "check_plan failed".
    If a new plan is available, it iterates through the guilds in `BSZ_BOT.guilds` and checks if the "routine" setting is enabled and if the "routine_channel_id" is not None.
    If the conditions are met, it creates a `discord.File` object with the filename of the plan's image file and sends it to the specified channel using `channel.send()`.
    The `simple_embed()` function is used to create an embed message with the title "Neuer Vertretungsplan!" and the file attachment.

    Parameters:
        None

    Returns:
        None
    """    
    logger.info("checking for new plans")
    for guild in BSZ_BOT.guilds:

        s = GuildSettings(guild)
        if s.get("routine") != True or s.get("routine_channel_id") == 0:
            continue
        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            continue

        plan = Plan(guild)

        if not await plan.new_plan_available():
            if plan.any_errors():
                if not s.get("error_last_time"):
                    await channel.send(embed=simple_embed(f"Error: {plan.get_error_code()}", f"""Could not fetch the new plan with: 
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
                s.set("error_last_time", True)
                logger.error(f"check_plan failed for {guild.name}")
                continue
            s.set("error_last_time", False)
            continue

        file = discord.File(f"{plan.get_file_name()}.png")
        await channel.send(file=file, embed=simple_embed('Neuer Vertretungsplan!', '', f"attachment://{plan.get_file_name()}.png"))
