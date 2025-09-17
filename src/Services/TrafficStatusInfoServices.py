from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime
from DBAccess.TrafficInfoDAL import *

def findAllTrafficStatusInfo():
    res = findAllTrafficStatusInfoDAL()
    for trafficStatusInfo in res:
        trafficStatusInfo['_id'] = str(trafficStatusInfo['_id'])
    return res, 200
    


def findTrafficStatusInfoByID(id):
    res = findTrafficStatusInfoByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    return res, 200


def insertTrafficStatusInfo(body):
    body = insertTrafficStatusInfoDAL(body)
    body['_id'] = str(body['_id'])
    return body, 201
def updateTrafficStatusInfo(body):
    body['_id'] = ObjectId(body['_id'])
    res = findTrafficStatusInfoByIDDAL(body['_id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    print(body)
    body = updateTrafficStatusInfoDAL(body)
    body['_id'] = str(body['_id'])
    return body, 201
def deleteTrafficStatusInfo(id):
    res = findTrafficStatusInfoByIDDAL(id)
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    deleteTrafficStatusInfoDAL(id)
    return jsonify({"message": "Successful"}), 200

    