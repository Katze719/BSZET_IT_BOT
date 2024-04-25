from discord.ext.commands import Command
from .core import BSZ_BOT
from .commands import ping

BSZ_BOT.tree.add_command(ping)
