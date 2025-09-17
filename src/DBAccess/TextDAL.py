from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import current_app

def findAllTextDAL():
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        res = textTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findTextByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        res = textTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findTextByDataIDListDAL(idlist):
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        objList = []
        for dataID in idlist: objList.append(ObjectId(dataID))
        res = textTable.find({"dataID": {'$in': objList}})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def insertTextDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        textTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateTextDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        textTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteTextDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        textTable = client.db["texts"]
        res = textTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e