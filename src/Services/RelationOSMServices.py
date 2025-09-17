from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from DBAccess.RelationOSMDAL import *

#Toàn bộ giá trị trả về trong phần Try đều phải trả về bằng tuple (res, statusCode)
#Toàn bộ dữ liệu không phải string thì update lại


#["id", "type", "location", "tags", "version", "timestamp", "changeset", "uid", "user"]
def findAllRelationOSM():
    res = findAllRelationOSMDAL()
    for relation in res:
        del relation['_id']
    return res, 200


def findRelationOSMByID(id):
    res = findRelationOSMByIDDAL(int(id))
    if res == None: return {}, 200
    del res['_id']
    return res, 200

def updateRelationOSM(body):
    try:
        client = TrafficMongoClient()
        relationOSMTable = client.db["relations"]
        res = relationOSMTable.find_one({"id": body['id']})
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        relationOSMTable.update_one({'id': body['id']}, {"$set": body})
        del body['id']
        return body, 201
    except PyMongoError as e:
        raise e
    finally:
        client.close()
    
