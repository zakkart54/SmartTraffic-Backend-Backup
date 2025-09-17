from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify


def findAllRelationOSMDAL():
    try:
        client = TrafficMongoClient()
        relationsTable = client.db["relations"]
        res = relationsTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findRelationOSMByIDDAL(id):
    try:
        client = TrafficMongoClient()
        relationsTable = client.db["relations"]
        print(type(id))
        res = relationsTable.find_one({"id": id})
        print(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()