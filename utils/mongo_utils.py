from datetime import datetime
import pymongo
from .contants import HOST_IP
# CLIENT = pymongo.MongoClient(
#     "mongodb://desktop-j5l1v77:27017/test?retryWrites=true&w=majority")
CLIENT = pymongo.MongoClient(
    f"mongodb://{HOST_IP}:27017/test?retryWrites=true&w=majority")
STOCK_ANALYSIS = CLIENT.stock_analysis

def update_by_keys(collections, samples=[], distinct_keys=None):
    if distinct_keys:
        for sample in samples:
            collections.replace_one(
                {key: sample.get(key) for key in distinct_keys}, sample, upsert=True)  # this api is very slow.


def delete_update_by_keys(collections, samples=[], distinct_keys=None):
    if distinct_keys and samples:
        sample = samples[0]
        delete_key = {key: sample.get(key) for key in ["scode"]}
        delet = collections.delete_many(delete_key)
        print(f"deleted {delet.deleted_count} sample under {delete_key} at {datetime.now()}")
        collections.insert_many(samples)
        print(f"inserted {len(samples)} sample at {datetime.now()}")


def get_collection_max(collection, group_key, value_key):
    return {sample['_id']: sample[value_key] for sample in collection.aggregate([
        {
            "$group":
            {
                "_id": f"${group_key}",
                value_key:
                {
                    "$max": f"${value_key}"
                }
            }
        }
    ])}


if __name__ == "__main__":
    from utils.holder_number import HolderNumber
    hn = HolderNumber()
    scode = 'sz000001'
    table = hn.get_holder_number_table(scode)
    print(table)
    for sample in list(table.T.to_dict().values()):
        STOCK_ANALYSIS.test.replace_one(
            {"date": sample["date"], "scode": sample["scode"]}, sample, upsert=True)
