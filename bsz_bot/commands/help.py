import discord
from ..helpers import *

commands_info = [
    {"command": "/help", "description": "Prints a list of available commands", "experimental": False, "admin": False},
    {"command": "/activate", "description": "Activates the bot", "experimental": False, "admin": True},
    {"command": "/deactivate", "description": "Deactivates the bot", "experimental": False, "admin": True},
    {"command": "/deactivate_experimental_features", "description": "Deactivates experimental features", "experimental": False, "admin": True},
    {"command": "/activate_experimental_features", "description": "Activates experimental features", "experimental": False, "admin": True},
    {"command": "/set <variable_name> <value>", "description": "Sets the specified variable to the given value", "experimental": False, "admin": True},
    {"command": "/reset", "description": "Resets all variables to their default values", "experimental": False, "admin": True},
    {"command": "/ping", "description": "Checks the bot's responsiveness", "experimental": False, "admin": False},
    {"command": "/plan", "description": "Retrieves the current plan", "experimental": False, "admin": False},
    {"command": "/get <variable_name>", "description": "Retrieves the value of the specified variable", "experimental": False, "admin": False},
    {"command": "/status", "description": "Checks if the bot is currently active", "experimental": False, "admin": False},
    {"command": "/feedback <message>", "description": "Submits user feedback", "experimental": False, "admin": False},
    {"command": "/print_parsed_table_experimental", "description": "Displays the parsed table", "experimental": True, "admin": False},
    {"command": "/news_experimental", "description": "Retrieves the latest news", "experimental": True, "admin": False},
]

@discord.app_commands.command(name="help", description="Print a list of available commands.")
async def help(ctx : discord.Interaction):
    embed = simple_embed("Available Commands", "Here is a list of all available commands:")

    for info in commands_info:
        experimental_note = " (Experimental)" if info["experimental"] else ""
        admin_note = " (Admin only)" if info["admin"] else ""
        embed.add_field(name=f"{info['command']}{admin_note}{experimental_note}", value=f"{info['description']}", inline=False)

    await ctx.response.send_message(embed=embed, ephemeral=True)