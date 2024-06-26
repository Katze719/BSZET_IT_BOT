from .tasks import setup_tasks
from .core import BSZ_BOT
from .commands import ping, plan, get, set, reset, changelog, activate, deactivate, status, print_parsed_table_beta, activate_beta_features, deactivate_beta_features, news, feedback, help, use_old_plan_sending_method, use_new_plan_sending_method
from .helpers import Plan, log, send_update_info

BSZ_BOT.tree.add_command(use_old_plan_sending_method)
BSZ_BOT.tree.add_command(use_new_plan_sending_method)
BSZ_BOT.tree.add_command(deactivate_beta_features)
BSZ_BOT.tree.add_command(print_parsed_table_beta)
BSZ_BOT.tree.add_command(activate_beta_features)
BSZ_BOT.tree.add_command(deactivate)
BSZ_BOT.tree.add_command(changelog)
BSZ_BOT.tree.add_command(feedback)
BSZ_BOT.tree.add_command(activate)
BSZ_BOT.tree.add_command(status)
BSZ_BOT.tree.add_command(reset)
BSZ_BOT.tree.add_command(ping)
BSZ_BOT.tree.add_command(plan)
BSZ_BOT.tree.add_command(news)
BSZ_BOT.tree.add_command(help)
BSZ_BOT.tree.add_command(get)
BSZ_BOT.tree.add_command(set)
