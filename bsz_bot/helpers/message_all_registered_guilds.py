import discord
from .settings import GuildSettings
from ..core import BSZ_BOT

async def message_all_registered_guilds(embed : discord.Embed):    
    for guild in BSZ_BOT.guilds:
        s = GuildSettings(guild.id)
        if s.get("routine_channel_id") == 0:
            continue

        channel = BSZ_BOT.get_channel(int(s.get("routine_channel_id")))
        if channel:
            await channel.send(embed=embed)