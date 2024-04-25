from .check_plan import check_plan

async def setup_tasks():
    check_plan.start()