from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify, current_app

def findAllReportDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find()
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e


def findAllvalidReportDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({"qualified": True})
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    
def findAllneededValidationReportDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({"eval": {"$gte": 0.3, "$lte": 0.8 }})
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    
def findAllinvalidReportDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({"eval": {"$lt": 0.3}})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e



def findMax100VerifiedReportDAL():
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({"qualified": True}).sort('createdDate', -1).limit(100)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findAllUnqualifiedReportDAL():
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({'qualified': False})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findReportByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        print(id)
        res = reportTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findReportByUploaderIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find({"uploaderID": ObjectId(id)})
        if res == None: return {}, 200
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findReportByDataImageIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find_one({"dataImgID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findReportDataTextIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.find_one({"dataTextID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def insertReportDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        print(body)
        reportTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateReportDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        reportTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteReportDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        reportTable = client.db["reports"]
        res = reportTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e