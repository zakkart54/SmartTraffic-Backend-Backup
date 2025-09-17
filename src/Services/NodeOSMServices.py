from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.NodeOSMDAL import *
from pymongo.errors import PyMongoError
from pymongo import GEOSPHERE
from bson.objectid import ObjectId
from flask import jsonify
#["id", "type", "location", "tags", "version", "timestamp", "changeset", "uid", "user"]
def findAllNodeOSM():
    res = findAllNodeOSMDAL()
    for i in res:
        del i['_id']
    return res, 200


def findNodeOSMbyCoor(a,b):
    res = findNodeOSMbyCoorDAL(a,b)
    if res == None: return {}, 200
    del res['_id']
    return res, 200


def findNodeOSMInSegmentbyCoor(a,b):
    res = findNodeOSMInSegmentbyCoorDAL(a,b)
    if res == None: return {}, 200
    del res['_id']
    return res, 200
    

def findNodeOSMsInSegmentbyCoor(a,b):
    res = findNodeOSMsInSegmentbyCoorDAL(a,b)
    for i in res:
        del i['_id']
    return res, 200

def findNodeOSMByID(id):
    print(id)
    res = findNodeOSMByIDDAL(id)
    if res == None: return {}, 200
    del res['_id']
    return res, 200

def updateNodeOSM(body):
    res = updateNodeOSMDAL(body)
    del res['_id']
    return res, 201
    
def findNodeIDsInBBox(lon_min, lat_min, lon_max, lat_max):
    nodes_in_bbox = findNodesInBBoxDAL(lon_min, lat_min, lon_max, lat_max)
    node_ids = [n["id"] for n in nodes_in_bbox]
    return node_ids


