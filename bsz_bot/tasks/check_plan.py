import discord
import os
from discord.ext import tasks
from ..core import BSZ_BOT
from ..helpers import *

async def check_plan__old(guild):
        s = GuildSettings(guild)
        if s.get("routine") != True or s.get("routine_channel_id") == 0:
            return
        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            return

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
                return
            s.set("error_last_time", False)
            return

        file = discord.File(f"{plan.get_file_name()}.png")
        await channel.send(file=file, embed=simple_embed('Neuer Vertretungsplan!', '', f"attachment://{plan.get_file_name()}.png"))

async def check_plan__new(guild):
        s = GuildSettings(guild)
        if s.get("routine") != True or s.get("routine_channel_id") == 0:
            return
        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if not channel:
            return

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
                return
            s.set("error_last_time", False)
            return

        parsed_plan = parse_table(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(guild).get_file_name()}.pdf')
        
        msg = ''

        for event in parsed_plan:
            if s.get("class") in event["class"]:
                msg += f"```txt\nAm {event['date']} {event['day']}\nStunde: {event["hours"]}\nLehrer: {event["teacher"]}\nFach:   {event["subject"]}\nRaum:   {event["room"]}\nInfo:   {event["info"]}\n```\n"

        if msg != '':
            await channel.send(embed=simple_embed('News', f"{msg}"))
        
@tasks.loop(minutes=5)
async def check_plan():
    logger.info("checking for new plans")
    for guild in BSZ_BOT.guilds:
        if GuildSettings(guild).get("use_old_plan_function"):
            await check_plan__old(guild)
        else:
            await check_plan__new(guild)
            