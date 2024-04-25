import discord
from ..helpers import *

# Die URL des PDF-Dokuments mit Benutzername und Passwort
pdf_url = "http://geschuetzt.bszet.de/s-lk-vw/Vertretungsplaene/vertretungsplan-bs-it.pdf"

# Benutzername und Passwort für die Authentifizierung
benutzername = "bsz-et-2324"
passwort = "schulleiter#23"

file_name = "vertretungsplan"

def get_plan_png():
    error_code = fetch_document(pdf_url, f"{file_name}.pdf", benutzername, passwort)

    if error_code != 200:
        return error_code

    return error_code


@discord.app_commands.command(name="plan")
async def plan(ctx : discord.Interaction):
    error_code = Plan(pdf_url, benutzername, passwort, file_name).download()
    if error_code != 200:
        await ctx.response.send_message(embed=simple_embed(f"request: {error_code}", "ERROR: the pdf document could not be downloaded (ask Paul D. for more Information)"))
        return
    file = discord.File(f"{file_name}.png")
    await ctx.response.send_message(file=file, embed=simple_embed('Aktueller Vertretungsplan', '', f"attachment://{file_name}.png"))


