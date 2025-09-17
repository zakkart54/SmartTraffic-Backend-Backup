from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import current_app

def findAllImagesDAL():
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        res = imageTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findImageByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        print(id)
        res = imageTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findImageByDataIDListDAL(idlist):
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        objList = []
        for dataID in idlist: objList.append(ObjectId(dataID))
        res = imageTable.find({"dataID": {'$in': objList}})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def insertImageDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        imageTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateImageDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        imageTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteImageDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        imageTable = client.db["images"]
        res = imageTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e