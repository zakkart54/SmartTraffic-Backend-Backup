from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify

def findAllReportDAL():
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findMax100VerifiedReportDAL():
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find({"qualified": True}).sort('createdDate', -1).limit(100)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findAllUnqualifiedReportDAL():
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find({'qualified': False})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findReportByIDDAL(id):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        print(id)
        res = reportTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findReportByUploaderIDDAL(id):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find({"uploaderID": ObjectId(id)})
        if res == None: return {}, 200
        res=list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()


def findReportByDataImageIDDAL(id):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find_one({"dataImgID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findReportDataTextIDDAL(id):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.find_one({"dataTextID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertReportDAL(body):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        print(body)
        reportTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateReportDAL(body):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        reportTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteReportDAL(id):
    try:
        client = TrafficMongoClient()
        reportTable = client.db["reports"]
        res = reportTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()