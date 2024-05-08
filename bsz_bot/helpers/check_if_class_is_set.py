import discord
from .settings import GuildSettings

def check_if_class_is_set(guild : discord.Guild) -> bool:
    return GuildSettings(guild).get("class")