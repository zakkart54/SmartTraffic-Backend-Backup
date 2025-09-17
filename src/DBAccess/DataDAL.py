from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify

def findAllDataDAL():
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findDataByIDDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findDataByUploaderIDDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find({"uploaderID": ObjectId(id)})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findDataByStatusInfoIDDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find_one({"statusID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findDataByImageIDDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        print(id)
        res = dataTable.find_one({"InfoID": ObjectId(id), "type": 'image'})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findDataByTextIDDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find_one({"InfoID": ObjectId(id), "type": 'text'})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertDataDAL(body):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        dataTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateDataDAL(body):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        print
        dataTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteDataDAL(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        dataTable.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Successful"})
    except PyMongoError as e:
        raise e
    finally:
        client.close()