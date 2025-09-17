from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime

def findAllTrafficStatusInfoDAL():
    try:
        client = TrafficMongoClient()
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findTrafficStatusInfoByIDDAL(id):
    try:
        client = TrafficMongoClient()
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertTrafficStatusInfoDAL(body):
    try:
        client = TrafficMongoClient()
        trafficStatusInfoTable = client.db["statusInfos"]
        trafficStatusInfoTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateTrafficStatusInfoDAL(body):
    try:
        client = TrafficMongoClient()
        trafficStatusInfoTable = client.db["statusInfos"]
        trafficStatusInfoTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteTrafficStatusInfoDAL(id):
    try:
        client = TrafficMongoClient()
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()