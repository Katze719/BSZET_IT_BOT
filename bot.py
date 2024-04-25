import discord
import src.document as document
import src.compare_pdf as compare_pdf
import src.table_parser as tp
import src.helpers as h
import src.settings as settings
import copy
import camelot
import datetime
import os
from src.log import logger
from discord.ext import commands, tasks
from discord import app_commands
from pdf2image import convert_from_path
from PIL import Image

HARD_ERROR=False

file_name = 'vertretungsplan'

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

changelog_embed=discord.Embed(title="Auto Update", url="https://github.com/Katze719/SchulBot/pkgs/container/schulbot", description="Version v3.0.0 -> Version v3.1.0", color=h.EMBED_COLOR)
changelog_embed.add_field(name="better error handling", value="der bot schreibt bei fehlern in den chat")

# Event handling

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Reddit"))
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.exception(e)
    plan__()
    check_plan.start()
        
# Event handling end


# commands
@bot.tree.command(name="ping")
async def ping(ctx):
    """
    Pingt den Bot ob er erreichbar ist.

    Usage:
    !ping
    """
    await ctx.response.send_message(embed=h.simple_embed(f"Pong! {round(bot.latency * 1000)}ms"))

def plan__():
    error_code = document.save_pdf_doc()

    if error_code != 200:
        return error_code

    images = convert_from_path(f"{file_name}.pdf")

    combined_image = Image.new('RGB', (images[0].width, sum(image.height for image in images)))

    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height

    combined_image.save(f'{file_name}.png', 'PNG')
    return error_code


@bot.tree.command(name="plan")
async def plan(ctx):
    """
    Sendet den Vertretungsplan als PNG bild zurück.

    Usage:
    !plan
    """
    error_code = plan__()
    if error_code != 200:
        await ctx.response.send_message(embed=h.simple_embed(f"request: {error_code}", "ERROR: the pdf document could not be downloaded (ask Paul D. for more Information)"))
        return
    file = discord.File(f"{file_name}.png")
    await ctx.response.send_message(file=file, embed=h.simple_embed('Aktueller Vertretungsplan', '', f"attachment://{file_name}.png"))

@bot.tree.command(name="set")
async def set(ctx, variable_name: str, value: str):
    s = settings.GuildSettings(ctx.guild.id)
    if variable_name in s.get_all_settings():
        s.set(variable_name, value)
        if variable_name == 'routine' and (value == 'True' or value == 'true'):
            s.set('routine', 'True')
            s.set('routine_channel_id', ctx.channel.id)
            await ctx.response.send_message(embed=h.simple_embed(f'Set {variable_name} and routine_channel_id', f"{variable_name} was set to {value} and routine_channel_id was set to {ctx.channel.id}"))
            return
        await ctx.response.send_message(embed=h.simple_embed(f'Set {variable_name}', f"{variable_name} was set to {value}"))
        return
    await ctx.response.send_message(embed=h.simple_embed(f'Set {variable_name}', f"{variable_name} Does not exist!"))

@bot.tree.command(name="get")
async def get(ctx, variable_name: str):
    s = settings.GuildSettings(ctx.guild.id)
    if variable_name == 'all':
        response = "```toml\n"
        for key, value in s.get_all_settings().items():
            response += f"{key} : {value}\n"
        response += "```"
        await ctx.response.send_message(embed=h.simple_embed('All vars', response))
        return
    value = s.get(variable_name)
    await ctx.response.send_message(embed=h.simple_embed(f'Get {variable_name}',f"{variable_name} : {value}"))

@bot.tree.command(name="reset")
async def reset(ctx):
    s = settings.GuildSettings(ctx.guild.id)
    s.settings.clear()
    s.save_settings()
    await ctx.response.send_message(embed=h.simple_embed("Reset!", 'success'))

@bot.tree.command(name="parse_table")
async def parse_table(ctx, class_name : str = '22/5'):
    await ctx.response.send_message(embed=h.simple_embed('Downloading ...'))
    plan__()
    await ctx.edit_original_response(embed=h.simple_embed('Parsing PDF ...'))
    tables = camelot.read_pdf(f"{file_name}.pdf", pages='all')   #address of file location
    await ctx.edit_original_response(embed=h.simple_embed('Parsing Tables ...'))
    # print the first table as Pandas DataFrame
    important = ''
    for table in tables:
        if class_name in table.df[6][0]:
            important += f"**{table.df.iat[0,0].replace('...', '')} {table.df.iat[0,1].replace('...', '')}**\n{tp.parse_table(table.df)}\n"
    if important == '':
        important = f"IT{class_name} steht nicht im aktuellen Vertretungsplan!"
    embed=h.simple_embed(f'Table (IT{class_name})', important)
    embed.set_footer(text=str(datetime.datetime.now()))
    await ctx.edit_original_response(embed=embed)

# @bot.tree.command(name="changelog")
# async def changelog(ctx):
#     await ctx.response.send_message(embed=changelog_embed)

async def send_to_all_guilds(msg : str):
    for guild in bot.guilds:
        if msg == "update":
            settings.GuildSettings(guild.id).set("name", guild.name)
        channel = bot.get_channel(int(settings.GuildSettings(guild.id).get("routine_channel_id")))
        if not channel:
            break
        if msg == "changelog":
            await channel.send(embed=changelog_embed)
        if msg == "error":
            await channel.send(embed=h.simple_embed(f"request: FAILED", "ERROR: the pdf document could not be downloaded (stacktrace dumped in console [`docker-compose logs schulbot | grep -i 'error' | tee -a ./error.log`])"))
        if msg == "recovered":
            await channel.send(embed=h.simple_embed(f"recovered!", "bot is now back online and working."))



@bot.tree.command(name="send_info_to_all_guilds")
async def send_info_to_all_guilds(ctx, password : str, msg : str):
    if password == "Katze719":
        await send_to_all_guilds(msg)
        await ctx.response.send_message(embed=h.simple_embed(msg, "Done"))
    else:
        await ctx.response.send_message(embed=h.simple_embed("wrong password!"))


# commands end

# tasks

@tasks.loop(minutes=5)
async def check_plan():
    # read old plan
    global HARD_ERROR
    old_file = compare_pdf.hash_read_file(f"{file_name}.pdf")

    # get new plan
    error_code = plan__()
    if error_code != 200:
        if HARD_ERROR:
            return
        logger.error("Downloading new Plan failed!")
        HARD_ERROR=True
        await send_to_all_guilds("error")
        return
    
    HARD_ERROR=False

    # read new plan
    new_file = compare_pdf.hash_read_file(f"{file_name}.pdf")

    # compare old with new plan
    logger.info("comparing old with new plan")
    if old_file == new_file:
        return
    

    # sending to channels
    for guild in bot.guilds:
        s = settings.GuildSettings(guild.id)
        if s.get("routine") != "True" or s.get("routine_channel_id") == None:
            continue
        file = discord.File(f"{file_name}.png")
        channel = bot.get_channel(int(s.get("routine_channel_id")))
        if channel:
            await channel.send(file=file, embed=h.simple_embed('Neuer Vertretungsplan!', '', f"attachment://{file_name}.png"))
            print(f"send plan to {s.get('routine_channel_id')} :D")
#tasks end

bot.run(os.environ['DISCORD_BOT_TOKEN'])
