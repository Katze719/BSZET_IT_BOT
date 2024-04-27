from .tasks import setup_tasks
from .core import BSZ_BOT
from .commands import ping, plan, get, set, reset, changelog, activate, deactivate
from .helpers import Plan, log, send_update_info

BSZ_BOT.tree.add_command(deactivate)
BSZ_BOT.tree.add_command(changelog)
BSZ_BOT.tree.add_command(activate)
BSZ_BOT.tree.add_command(reset)
BSZ_BOT.tree.add_command(ping)
BSZ_BOT.tree.add_command(plan)
BSZ_BOT.tree.add_command(get)
BSZ_BOT.tree.add_command(set)
