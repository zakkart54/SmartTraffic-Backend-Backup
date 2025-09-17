from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify
def findAllNotificationsDAL():
    try:
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNotificationsByIDDAL(id):
    try:
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNotificationsByUserIDDAL(id):
    try:
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find({"userID": ObjectId(id)})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNotificationsByContentDAL(content):
    try:
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find_one({"content": content})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def insertNotificationsDAL(body):
    try:
        print(body)
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        notificationsTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateNotificationsDAL(body):
    try:
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        notificationsTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteNotificationsDAL(id):
    try:
        res = findNotificationsByIDDAL(id)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        client = TrafficMongoClient()
        notificationsTable = client.db["notifications"]
        res = notificationsTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()