from pymongo.errors import PyMongoError
from flask import current_app

def findAllWayOSMDAL():
    try:
        client = current_app.config['DB_CLIENT']
        wayOSMTable = client.db["wayOSM"]
        res = wayOSMTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findWayOSMByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        wayOSMTable = client.db["wayOSM"]
        res = wayOSMTable.find_one({"id": id})
        return res
    except PyMongoError as e:
        raise e

def updateWayOSMDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        wayOSMTable = client.db["wayOSM"]
        wayOSMTable.update_one({'id': body['id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e