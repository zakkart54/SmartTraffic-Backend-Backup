from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify, current_app
def findAllNotificationsDAL():
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findNotificationsByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e

def findNotificationsByUserIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find({"userID": {"$in": [ObjectId(id)]}}).sort("timestamp", -1)
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findNotificationsByContentDAL(content):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        res = notificationsTable.find_one({"content": content})
        return res
    except PyMongoError as e:
        raise e

def insertNotificationsDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        notificationsTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e

def updateNotificationsDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        notificationsTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def deleteNotificationsDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        notificationsTable = client.db["notifications"]
        res = findNotificationsByIDDAL(id)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        res = notificationsTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
