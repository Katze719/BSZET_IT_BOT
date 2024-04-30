import discord
import os
from bsz_bot import BSZ_BOT, setup_tasks, send_update_info, Plan, log

os.environ['SETTINGS_VOLUME'] = '/settings'

SUBSTITUTION_PLAN_PDF_URL = "https://geschuetzt.bszet.de/s-lk-vw/Vertretungsplaene/vertretungsplan-bs-it.pdf"

# Benutzername und Passwort für die Authentifizierung
USERNAME = "bsz-et-2324"
PASSWORD = "schulleiter#23"

CURRENT_VERSION = "v4.2.3"
CURRENT_VERSION_FILE = f"{os.getenv('SETTINGS_VOLUME')}/version.txt"

if __name__ == '__main__':
    Plan.save_settings(SUBSTITUTION_PLAN_PDF_URL, USERNAME, PASSWORD)
    
    @BSZ_BOT.event
    async def on_ready():
        log.logger.info(f'Bot is ready! Logged in as {BSZ_BOT.user}')
        await BSZ_BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=CURRENT_VERSION))
        try:
            synced = await BSZ_BOT.tree.sync()
            log.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            log.logger.exception(e)
        await setup_tasks()

        await send_update_info(CURRENT_VERSION, CURRENT_VERSION_FILE)

    BSZ_BOT.run(os.getenv('DISCORD_BOT_TOKEN'))
