from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import current_app, jsonify

def findAllNodeOSMDAL():
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findNodeOSMbyCoorDAL(a,b):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find_one({
            "type": "node",
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [a, b]
                    },
                    "$maxDistance": 1000
                }
            }
        })
        return res
    except PyMongoError as e:
        raise e

def findNodeOSMInSegmentbyCoorDAL(a,b):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find_one({
            "type": "node",
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [a, b]
                    },
                    "$maxDistance": 1000
                }
            },
            "belongs_to_segments": {"$exists": True, "$ne": []}
        })
        return res
    except PyMongoError as e:
        raise e

def findNodeOSMsInSegmentbyCoorDAL(a,b):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find({
            "type": "node",
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [a, b]
                    },
                    "$maxDistance": 5000
                }
            },
            "belongs_to_segments": {"$exists": True, "$ne": []}
        }).limit(50)
        return list(res)
    except PyMongoError as e:
        raise e

def findNodeOSMByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find_one({"type": "node","id": id})
        return res
    except PyMongoError as e:
        raise e

def updateNodeOSMDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        body = nodeOSMTable.update_one({'id': body['id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e

def findNodesInBBoxDAL(lon_min, lat_min, lon_max, lat_max):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        nodes_in_bbox = list(nodeOSMTable.find(
            {
                "location": {
                    "$geoWithin": {
                        "$box": [
                            [lon_min, lat_min],
                            [lon_max, lat_max]
                        ]
                    }
                }
            },
            {"id": 1, "location.coordinates": 1}
        ))
        return nodes_in_bbox
    except PyMongoError as e:
        raise e

def findNodesOSMByIDsDAL(ids: list[int]):
    try:
        client = current_app.config['DB_CLIENT']
        nodeOSMTable = client.db["nodes"]
        cursor = nodeOSMTable.find(
            {"id": {"$in": ids}},
            {"id": 1, "location.coordinates": 1}
        )
        res = list(cursor)
        return res
    except PyMongoError as e:
        raise e