import discord
from ..helpers import *

def parse_changelog():
    """
    Parses the CHANGELOG.txt file to retrieve the latest changelog entry.

    Returns:
        str: The latest changelog entry.

    Raises:
        FileNotFoundError: If the CHANGELOG.txt file is not found.
        Exception: If there is an error reading the changelog.
    """
    try:
        with open('CHANGELOG.txt', 'r') as file:
            content = file.read()
            end_index = content.find('---')
            if end_index != -1:
                latest_entry = content[:end_index].strip()
            else:
                latest_entry = content.strip()
            return latest_entry
    except FileNotFoundError:
        return "CHANGELOG.txt file not found."
    except Exception as e:
        return f"Error reading the changelog: {str(e)}"
    
@discord.app_commands.command(name="changelog", description="Gives you the latest changelog entry.")
async def changelog(ctx: discord.Interaction):
    """
    Gives you the latest changelog entry.

    Parameters:
        ctx (discord.Interaction): The interaction context.

    Returns:
        None
    """
    latest_changelog = parse_changelog()
    if "Error" in latest_changelog or "not found" in latest_changelog:
        await ctx.response.send_message(embed=simple_embed("Error!", latest_changelog))
    else:
        if len(latest_changelog) > 2048:
            latest_changelog = latest_changelog[:2045] + "..."
        await ctx.response.send_message(embed=simple_embed("Latest Changelog", f"[View the full changelog here](https://github.com/Katze719/BSZET_IT_BOT/blob/main/CHANGELOG.txt)\n\n{latest_changelog}"))
