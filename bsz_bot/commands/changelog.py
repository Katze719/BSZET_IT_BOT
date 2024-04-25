import discord
from ..helpers import *

def parse_changelog():
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
    latest_changelog = parse_changelog()
    if "Error" in latest_changelog or "not found" in latest_changelog:
        await ctx.response.send_message(embed=simple_embed("Error!", latest_changelog))
    else:
        if len(latest_changelog) > 2048:
            latest_changelog = latest_changelog[:2045] + "..."
        await ctx.response.send_message(embed=simple_embed("Latest Changelog", f"[View the latest changelog here](https://github.com/Katze719/BSZET_IT_BOT)\n\n{latest_changelog}"))
