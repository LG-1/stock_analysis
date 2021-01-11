import pymongo
CLIENT = pymongo.MongoClient(
    "mongodb://desktop-j5l1v77:27017/test?retryWrites=true&w=majority")
STOCK_ANALYSIS = CLIENT.stock_analysis

def update_by_keys(collections, samples=[], distinct_keys=None):
    if distinct_keys:
        for sample in samples:
            collections.update(
                {key: sample.get(key) for key in distinct_keys}, sample, upsert=True)


if __name__ == "__main__":
    from utils.holder_number import HolderNumber
    hn = HolderNumber()
    scode = 'sh689009'
    table = hn.get_holder_number_table(scode)
    print(table)
    for sample in list(table.T.to_dict().values()):
        STOCK_ANALYSIS.test.update(
            {"date": sample["date"], "scode": sample["scode"]}, sample, upsert=True)
