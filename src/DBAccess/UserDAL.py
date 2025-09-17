from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime, timedelta


def findUserDAL(body):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        account = userTable.find_one({"username": body["username"]})
        return account
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def createRefreshTokenDAL(account,refresh_token):
    try:
        client = TrafficMongoClient()
        refreshTokenTable = client.db['refreshTokens']
        print(datetime.now() + timedelta(days=7))
        res = refreshTokenTable.insert_one({
            "token": refresh_token,
            "userID": account["_id"],
            "username": account["username"],
            "expiredAt": datetime.now() + timedelta(days=7)
        })
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findRefreshTokenDAL(body):
    try:
        client = TrafficMongoClient()
        refreshTokenTable = client.db['refreshTokens']
        print({
            "token": body["token"],
            "userID": body["_id"],
            "username": body["username"],
            "expiredAt": {'$gt': datetime.now()}
        })
        refresh_token =  refreshTokenTable.find_one({
            "token": body["token"],
            "userID": ObjectId(body["_id"]),
            "username": body["username"],
            "expiredAt": {'$gt': datetime.now()}
        })
        del refresh_token['_id']
        return refresh_token
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findAllUserDAL():
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        res = userTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findUserByIDDAL(id):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        res = userTable.find_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findUserByUsernameDAL(username):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        res = userTable.find_one({"username": username})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()


def insertUserDAL(body):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        userTable.insert_one(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateUserDAL(body):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        userTable.update_one({'_id': body['_id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteUserDAL(id):
    try:
        client = TrafficMongoClient()
        userTable = client.db["users"]
        res = userTable.delete_one({"_id": ObjectId(id)})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()
