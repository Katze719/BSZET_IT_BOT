import discord
import os
from bsz_bot import BSZ_BOT, setup_tasks, Plan, log

pdf_url = "http://geschuetzt.bszet.de/s-lk-vw/Vertretungsplaene/vertretungsplan-bs-it.pdf"

# Benutzername und Passwort für die Authentifizierung
benutzername = "bsz-et-2324"
passwort = "schulleiter#23"

file_name = "vertretungsplan"

if __name__ == '__main__':
    Plan.save_settings(pdf_url, benutzername, passwort, file_name)
    
    @BSZ_BOT.event
    async def on_ready():
        log.logger.info(f'Bot is ready! Logged in as {BSZ_BOT.user}')
        await BSZ_BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Reddit"))
        try:
            synced = await BSZ_BOT.tree.sync()
            log.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            log.logger.exception(e)
        await setup_tasks()

    BSZ_BOT.run(os.environ['DISCORD_BOT_TOKEN'])
