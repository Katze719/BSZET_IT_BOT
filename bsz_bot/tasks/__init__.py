from .check_plan import check_plan
from .check_parsed_plan_beta import get_news

async def setup_tasks():
    check_plan.start()
    get_news.start()
