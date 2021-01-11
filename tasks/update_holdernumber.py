from utils.stock_markets import get_all_codes

from utils.holder_number import HolderNumber
from utils.mongo_utils import update_by_keys
from utils.mongo_utils import STOCK_ANALYSIS


def update_holdernumber():
    hn = HolderNumber()
    all_codes = get_all_codes()

    for ts_code in all_codes[::-1]:
        print(ts_code)
        table = hn.get_holder_number_table(ts_code)
        update_by_keys(STOCK_ANALYSIS.holder_number,
                       samples=list(table.T.to_dict().values()),
                       distinct_keys=['date', 'scode'])
        

if __name__ == "__main__":
    update_holdernumber()
