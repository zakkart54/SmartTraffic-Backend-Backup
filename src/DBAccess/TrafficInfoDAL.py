from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import current_app

def findAllTrafficStatusInfoDAL():
    try:
        client = current_app.config['DB_CLIENT']
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findTrafficStatusInfoByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def insertTrafficStatusInfoDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        trafficStatusInfoTable = client.db["statusInfos"]
        trafficStatusInfoTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateTrafficStatusInfoDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        trafficStatusInfoTable = client.db["statusInfos"]
        trafficStatusInfoTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteTrafficStatusInfoDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        trafficStatusInfoTable = client.db["statusInfos"]
        res = trafficStatusInfoTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e