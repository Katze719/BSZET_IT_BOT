import discord
import os
import secrets
import string
from ..helpers import *
import aiofiles

def secure_random_string(length: int = 6) -> str:
    """
    Erstellt einen kryptographisch sicheren, zufälligen String der angegebenen Länge.
    
    :param length: Die Länge des zu erstellenden zufälligen Strings (Standard ist 6).
    :return: Ein sicher zufälliger String mit Groß- und Kleinbuchstaben sowie Ziffern.
    """
    # Alle möglichen Zeichen: Großbuchstaben, Kleinbuchstaben und Ziffern
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

async def async_copy(source, destination, buffer_size=1024*1024):
    """
    Kopiert eine Datei asynchron von `source` nach `destination`.
    
    :param source: Pfad zur Quelldatei
    :param destination: Pfad zur Zieldatei
    :param buffer_size: Größe des Puffers für das Lesen und Schreiben
    """
    async with aiofiles.open(source, mode='rb') as src, aiofiles.open(destination, mode='wb') as dst:
        while True:
            chunk = await src.read(buffer_size)
            if not chunk:
                break
            await dst.write(chunk)

@discord.app_commands.command(name="feedback", description="Write feedback to the Active Developers.")
async def feedback(ctx : discord.Interaction, msg : str):
    hash = secure_random_string(6)

    with open(f'{os.getenv("SETTINGS_VOLUME")}/feedback.txt', 'a') as f:
        f.write(f"{hash} - {ctx.user} - {ctx.guild.id} - {GuildSettings(ctx.guild).get("class")} : {msg}\n")

    await async_copy(f'{os.getenv("SETTINGS_VOLUME")}/{Plan(ctx.guild).get_file_name()}.pdf', f'{os.getenv("SETTINGS_VOLUME")}/{Plan(ctx.guild).get_file_name()}_{hash}.pdf')

    await ctx.response.send_message(embed=simple_embed(f'Feedback Sent!', 'Thank you for your feedback!'), ephemeral=True)
