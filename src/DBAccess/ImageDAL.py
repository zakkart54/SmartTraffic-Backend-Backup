from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

def findAllImagesDAL():
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        res = imageTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findImageByIDDAL(id):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        print(id)
        res = imageTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findImageByDataIDListDAL(idlist):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        objList = []
        for dataID in idlist: objList.append(ObjectId(dataID))
        res = imageTable.find({"dataID": {'$in': objList}})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertImageDAL(body):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        imageTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateImageDAL(body):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        imageTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteImageDAL(body):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        res = imageTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()