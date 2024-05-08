from .check_plan import check_plan
from .check_parsed_plan_beta import daily_task

async def setup_tasks():
    check_plan.start()
    daily_task.start()
