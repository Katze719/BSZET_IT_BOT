import discord
from ..helpers import *

commands_info = [
    {"command": "/help", "description": "Prints a list of available commands", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/activate", "description": "Activates the bot", "experimental": False, "admin": True, "needs_class": True},
    {"command": "/deactivate", "description": "Deactivates the bot", "experimental": False, "admin": True, "needs_class": False},
    {"command": "/deactivate_experimental_features", "description": "Deactivates experimental features", "experimental": False, "admin": True, "needs_class": True},
    {"command": "/activate_experimental_features", "description": "Activates experimental features", "experimental": False, "admin": True, "needs_class": True},
    {"command": "/set <variable_name> <value>", "description": "Sets the specified variable to the given value", "experimental": False, "admin": True, "needs_class": False},
    {"command": "/reset", "description": "Resets all variables to their default values", "experimental": False, "admin": True, "needs_class": False},
    {"command": "/ping", "description": "Checks the bot's responsiveness", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/plan", "description": "Retrieves the current plan", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/get <variable_name>", "description": "Retrieves the value of the specified variable", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/status", "description": "Checks if the bot is currently active", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/feedback <message>", "description": "Submits user feedback", "experimental": False, "admin": False, "needs_class": False},
    {"command": "/print_parsed_table", "description": "Displays the parsed table", "experimental": False, "admin": False, "needs_class": True},
    {"command": "/news", "description": "Retrieves the latest news", "experimental": False, "admin": False, "needs_class": True},
    {"command": "/use_new_plan_sending_method", "description": "Use the new plan sending method", "experimental": False, "admin": True, "needs_class": True},
    {"command": "/use_old_plan_sending_method", "description": "Use the old plan sending method", "experimental": False, "admin": True, "needs_class": False},
]

@discord.app_commands.command(name="help", description="Print a list of available commands.")
async def help(ctx : discord.Interaction):
    embed = simple_embed("Available Commands", "Here is a list of all available commands:")

    for info in commands_info:
        experimental_note = " (Experimental)" if info["experimental"] else ""
        admin_note = " (Admin only)" if info["admin"] else ""
        needs_class = " (Requires class)" if info["needs_class"] else ""
        embed.add_field(name=f"{info['command']}{admin_note}{needs_class}{experimental_note}", value=f"{info['description']}", inline=False)

    await ctx.response.send_message(embed=embed, ephemeral=True)