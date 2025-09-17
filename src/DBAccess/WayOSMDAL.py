from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from DBAccess.WayOSMDAL import *

def findAllWayOSMDAL():
    try:
        client = TrafficMongoClient()
        wayOSMTable = client.db["wayOSM"]
        res = wayOSMTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findWayOSMByIDDAL(id):
    try:
        client = TrafficMongoClient()
        wayOSMTable = client.db["wayOSM"]
        res = wayOSMTable.find_one({"id": id})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateWayOSMDAL(body):
    try:
        client = TrafficMongoClient()
        wayOSMTable = client.db["wayOSM"]
        wayOSMTable.update_one({'id': body['id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()
