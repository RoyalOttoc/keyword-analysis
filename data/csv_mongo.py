import json
import pandas as pd
from pymongo import MongoClient

df = pd.read_csv(r'./NDIS_private.csv')
df.to_json(r'NDIS_private.json')

client = MongoClient('localhost', 27017)
db = client.db
collection = db.collection

file_name = "./NDIS_private.json"
with open(file_name) as f:
    file_data = json.load(f)  # load data from JSON to dict
    for k, v in file_data.items():  # iterate over key-value pairs
        collection.insert_one(v)  # your collection object here
