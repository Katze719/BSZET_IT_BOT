import os
from .message_all_registered_guilds import message_all_registered_guilds
from ..commands.changelog import parse_changelog
from .simple_embed import simple_embed

def check_version_change(current_version : str, version_file : str = 'version.txt'):
    """
    Check if the current version has changed by comparing it with the last saved version.
    
    Parameters:
        current_version (str): The current version to check.
        version_file (str): The file where the last version is saved. Default is 'version.txt'.
    
    Returns:
        bool: True if the current version is different from the last saved version, False otherwise.
    """
    if os.path.exists(version_file):
        with open(version_file, 'r') as file:
            last_version = file.read().strip()
    else:
        last_version = None

    with open(version_file, 'w') as file:
        file.write(current_version)

    return last_version != current_version, last_version

async def send_update_info(current_version : str, version_file : str = 'version.txt'):
    """
    Asynchronously sends update information to all registered guilds if the current version has changed.
    
    Args:
        current_version (str): The current version to check.
        version_file (str): The file where the last version is saved. Default is 'version.txt'.
    
    Returns:
        None
    """
    info = check_version_change(current_version, version_file)
    if not info[0]:
        return
    
    await message_all_registered_guilds(simple_embed(f'Auto Update Information\n{info[1]} -> {current_version}', f"[View the full changelog here](https://github.com/Katze719/BSZET_IT_BOT/blob/main/CHANGELOG.txt)\n\n{parse_changelog()}"))

    
