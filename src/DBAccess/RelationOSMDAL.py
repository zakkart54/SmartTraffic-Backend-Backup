from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import current_app

def findAllRelationOSMDAL():
    try:
        client = current_app.config['DB_CLIENT']
        relationsTable = client.db["relations"]
        res = relationsTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findRelationOSMByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        relationsTable = client.db["relations"]
        print(type(id))
        res = relationsTable.find_one({"id": id})
        print(res)
        return res
    except PyMongoError as e:
        raise e