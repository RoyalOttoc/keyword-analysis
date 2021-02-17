from pymongo import MongoClient
import os

client = MongoClient("mongodb+srv://test:test@cluster0.pkhxf.mongodb.net/ndisdata?retryWrites=true&w=majority")
db = client.ndisdata
collection = db.private

def connect():
    os.system(
        "mongoimport --host cluster0-shard-00-02.pkhxf.mongodb.net:27017 --ssl -u test -p 'test' --authenticationDatabase admin  -d ndisdata -c private --type csv --drop --file data/NDIS_private.csv --headerline")

