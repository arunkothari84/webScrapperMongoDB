import pandas as pd
import json
import mongoDBClient


# Check weather the mongo db has same db or not.
def mongoDB(searchQuery):
    db = mongoDBClient.get_client()
    if searchQuery not in db.list_collection_names():
        return 'NOT EXIST'
    else:
        return "EXIST"


# Insert object if it is not already there
def mongoInsert(searchQuery):
    db = mongoDBClient.get_client()
    coll = db[searchQuery]
    data = pd.read_csv('products.txt', sep='\t')
    data_json = json.loads(data.to_json(orient='records'))
    coll.insert_many(data_json)


if __name__ == '__main__':
    mongoInsert('ps5')

