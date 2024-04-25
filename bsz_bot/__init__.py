from .tasks import setup_tasks
from .core import BSZ_BOT
from .commands import ping, plan, get, set, reset, changelog
from .helpers import Plan, log

BSZ_BOT.tree.add_command(changelog)
BSZ_BOT.tree.add_command(reset)
BSZ_BOT.tree.add_command(ping)
BSZ_BOT.tree.add_command(plan)
BSZ_BOT.tree.add_command(get)
BSZ_BOT.tree.add_command(set)
