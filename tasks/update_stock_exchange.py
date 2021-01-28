from celery import shared_task

from utils.stock_markets import get_stock_exchange_data
from utils.stock_markets import get_all_codes, lower_number2number_dot_upper
from utils.mongo_utils import STOCK_ANALYSIS, update_by_keys


def update_stock_prices_rzrq(*args, **kwargs):
    
    all_codes = get_all_codes()

    # update holder numder detail data
    for ts_code in all_codes:
        ts_code = lower_number2number_dot_upper(ts_code, days=kwargs.get('days', 720))
        print(ts_code)
        table = get_stock_exchange_data(ts_code)
        update_by_keys(STOCK_ANALYSIS.stock_price_rzrq,
                    samples=list(table.T.to_dict().values()),
                    distinct_keys=['scode', 'trade_date'])


@shared_task
def all_stock_tasks(*args, **kwargs):
    update_stock_prices_rzrq(*args, **kwargs)


if __name__ == "__main__":
    update_stock_prices_rzrq()