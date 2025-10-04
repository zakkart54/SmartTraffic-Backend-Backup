from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify, current_app

def findAllDataDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find()
        total = dataTable.estimated_document_count()
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res, total
    except PyMongoError as e:
        raise e
    
def findAllImgDataDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find({"type": 'image'})
        total = dataTable.count_documents({"type": 'image'})
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res, total
    except PyMongoError as e:
        raise e

def findAllTextDataDAL(limit=None,offset=None):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find({"type": 'text'})
        total = dataTable.count_documents({"type": 'text'})
        if offset: res = res.skip(offset)
        if limit: res = res.limit(limit)
        res = list(res)
        return res, total
    except PyMongoError as e:
        raise e

def findDataByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findDataByUploaderIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find({"uploaderID": ObjectId(id)})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findDataByStatusInfoIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find_one({"statusID": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findDataByImageIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        print(id)
        res = dataTable.find_one({"InfoID": ObjectId(id), "type": 'image'})
        return res
    except PyMongoError as e:
        raise e

def findDataByTextIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        res = dataTable.find_one({"InfoID": ObjectId(id), "type": 'text'})
        return res
    except PyMongoError as e:
        raise e

def insertDataDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        dataTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateDataDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        dataTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteDataDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        dataTable = client.db["data"]
        dataTable.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Successful"})
    except PyMongoError as e:
        raise e