from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify



def findAllTextDAL():
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        res = textTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findTextByIDDAL(id):
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        res = textTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findTextByDataIDListDAL(idlist):
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        objList = []
        for dataID in idlist: objList.append(ObjectId(dataID))
        res = textTable.find({"dataID": {'$in': objList}})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertTextDAL(body):
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        textTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateTextDAL(body):
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        textTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteTextDAL(id):
    try:
        client = TrafficMongoClient()
        textTable = client.db["texts"]
        res = textTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()