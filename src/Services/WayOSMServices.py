from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from DBAccess.WayOSMDAL import *

#["id", "type", "location", "tags", "version", "timestamp", "changeset", "uid", "user"]
def findAllWayOSM():
    res = findAllWayOSMDAL()
    for wayOSM in res:
        del wayOSM['_id']
    return res, 200


def findWayOSMByID(id):
    res = findWayOSMByIDDAL(id)
    if res == None: return {}, 200
    return res, 200

def updateWayOSM(body):
    res = findWayOSMByIDDAL(body['id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    body = updateWayOSMDAL(body)
    del body['id']
    return body, 201

