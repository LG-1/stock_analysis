import time
from datetime import datetime
from utils.stock_markets import get_all_codes

from utils.holder_number import HolderNumber
from utils.mongo_utils import update_by_keys, get_collection_max
from utils.mongo_utils import STOCK_ANALYSIS
from features.holders import holder_num_score

from utils.utils import write_pickle

hn = HolderNumber()

def update_holdernumber():
    
    all_codes = get_all_codes()
    codes_update = get_collection_max(STOCK_ANALYSIS.holder_number, 'scode', 'update_timestamp')

    # update holder numder detail data
    for ts_code in all_codes:
        print(ts_code)
        time_internal = 5*24*60*60  # 5 days
        update_time = codes_update.get(ts_code)
        update_time = update_time if isinstance(update_time, float) else 0
        if time.time() - update_time > time_internal:
            table = hn.get_holder_number_table(ts_code)
            update_by_keys(STOCK_ANALYSIS.holder_number,
                        samples=list(table.T.to_dict().values()),
                        distinct_keys=['date', 'scode'])


def update_holdernumber_score():
    """
    generate total market stock holder number change score.

    mind 2021-01-23 @LG TODO:
        number down, score up
    """
    all_codes = get_all_codes()
    scores_update = get_collection_max(STOCK_ANALYSIS.holder_number_score, 'scode', 'update_timestamp')
    # update holder numder change score
    for ts_code in all_codes:
        print(ts_code)
        time_internal = 12*60*60  # 12 hrs
        update_time = scores_update.get(ts_code)
        update_time = update_time if isinstance(update_time, float) else 0

        if time.time() - update_time > time_internal:
            table = hn.get_holder_number_table_from_mongo(ts_code)
            score = holder_num_score(table, [0.4, 0.3, 0.2, 0.1])
            sample = {"scode": ts_code, "compute_date": str(datetime.now().date()), "score": score, "update_timestamp": time.time()}
            update_by_keys(STOCK_ANALYSIS.holder_number_score, samples=[sample], distinct_keys=['scode', 'compute_date'])
    
    # dump holder score for futrue use.
    print(f"dumping all_holder_num_scores-{str(datetime.now().date())}.pkl")
    scores_update = get_collection_max(STOCK_ANALYSIS.holder_number_score, 'scode', 'compute_date')
    all_holder_num_scores = {scode: STOCK_ANALYSIS.holder_number_score.find_one({"scode": scode, "compute_date": compute_date}).get("score") for scode, compute_date in scores_update.items()}
    write_pickle(all_holder_num_scores, "notebooks/input/all_holder_num_scores.pkl")
    write_pickle(all_holder_num_scores, f"notebooks/input/all_holder_num_scores-{str(datetime.now().date())}.pkl")
        

def all_holder_tasks():
    update_holdernumber()
    update_holdernumber_score()

if __name__ == "__main__":
    # update_holdernumber()
    # update_holdernumber_score()
    all_holder_tasks()
