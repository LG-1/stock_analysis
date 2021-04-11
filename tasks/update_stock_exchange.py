import time
from celery import shared_task

from concurrent import futures

from utils.stock_markets import get_stock_exchange_data
from utils.stock_markets import get_all_codes, lower_number2number_dot_upper
from utils.mongo_utils import STOCK_ANALYSIS, update_by_keys, delete_update_by_keys


def update_stock_prices_rzrq(*args, **kwargs):
    
    all_codes = [lower_number2number_dot_upper(ts_code) for ts_code in get_all_codes()]
    details_all = []

    # # update holder numder detail data
    # for ts_code in all_codes:
    #     days = kwargs.get('days', 720)
    #     print(ts_code)
    #     details_single = []


    #     details_single = get_stock_exchange_data(ts_code, days=days)
    #     # details_single = get_stock_exchange_data.s(ts_code, days=days).apply_async()
    #     try:
    #         details_single = get_stock_exchange_data.apply_async(
    #             args=[ts_code], kwargs={"days": days}, retries=3).get()
            
    #     except Exception as e:
    #         pass

    #     details_all.extend(details_single)

    sub_num = 75
    for i in range(len(all_codes)//sub_num + 1):
        details_sub = []
        start_time = time.time()
        temp_codes = all_codes[i*sub_num: (i+1)*sub_num]
    
        with futures.ProcessPoolExecutor(max_workers=1) as pool:
            for details_single in pool.map(get_stock_exchange_data, temp_codes):
                # details_sub.extend(details_single)

                delete_update_by_keys(STOCK_ANALYSIS.stock_price_rzrq,
                                    samples=details_single,
                                    distinct_keys=['scode', 'trade_date'])
        end_time = time.time()
        print(f"sleeping {60-end_time+start_time}")
        time.sleep(max(0, 60-end_time+start_time))



@shared_task
def all_stock_tasks(*args, **kwargs):
    update_stock_prices_rzrq(*args, **kwargs)


if __name__ == "__main__":
    update_stock_prices_rzrq()
