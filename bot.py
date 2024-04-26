import discord
import os
from bsz_bot import BSZ_BOT, setup_tasks, send_update_info, Plan, log

SUBSTITUTION_PLAN_PDF_URL = "http://geschuetzt.bszet.de/s-lk-vw/Vertretungsplaene/vertretungsplan-bs-it.pdf"
SUBSTITUTION_PLAN_FILENAME = "vertretungsplan"

# Benutzername und Passwort für die Authentifizierung
USERNAME = "bsz-et-2324"
PASSWORD = "schulleiter#23"

CURRENT_VERSION = "v4.2.0rc"
CURRENT_VERSION_FILE = "/settings/version.txt"

if __name__ == '__main__':
    Plan.save_settings(SUBSTITUTION_PLAN_PDF_URL, USERNAME, PASSWORD, SUBSTITUTION_PLAN_FILENAME)
    
    @BSZ_BOT.event
    async def on_ready():
        log.logger.info(f'Bot is ready! Logged in as {BSZ_BOT.user}')
        await BSZ_BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Reddit"))
        try:
            synced = await BSZ_BOT.tree.sync()
            log.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            log.logger.exception(e)
        Plan().download() # first fetch because of a racecondition between the check_plan task and the normal Plan class
        await setup_tasks()

        await send_update_info(CURRENT_VERSION, CURRENT_VERSION_FILE)

    BSZ_BOT.run(os.environ['DISCORD_BOT_TOKEN'])
