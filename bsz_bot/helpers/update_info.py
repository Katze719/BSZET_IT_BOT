import os
from .message_all_registered_guilds import message_all_registered_guilds
from ..commands.changelog import parse_changelog
from .simple_embed import simple_embed

def check_version_change(current_version : str, version_file : str = 'version.txt'):
    if os.path.exists(version_file):
        with open(version_file, 'r') as file:
            last_version = file.read().strip()
    else:
        last_version = None

    with open(version_file, 'w') as file:
        file.write(current_version)

    return last_version != current_version

async def send_update_info(current_version : str, version_file : str = 'version.txt'):
    if not check_version_change(current_version, version_file):
        return
    
    await message_all_registered_guilds(simple_embed('Auto Update Information', f"[View the latest changelog here](https://github.com/Katze719/BSZET_IT_BOT)\n\n{parse_changelog()}"))

    
