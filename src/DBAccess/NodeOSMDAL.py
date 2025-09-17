from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify

def findAllNodeOSMDAL():
    try:
        client = TrafficMongoClient()
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNodeOSMbyCoorDAL(a,b):
    try:
        client = TrafficMongoClient()
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find_one({
            "type": "node",
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [a, b]
                    },
                    "$maxDistance": 1000  # Giới hạn bán kính 1000 mét
                }
            }
        })
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNodeOSMInSegmentbyCoorDAL(a,b):
    try:
        client = TrafficMongoClient()
        nodeOSMTable = client.db["nodes"]
        res = nodeOSMTable.find_one({
            "type": "node",
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [a, b]
                    },
                    "$maxDistance": 1000  # Giới hạn bán kính 1000 mét
                }
            },
            "belongs_to_segments": {"$exists": True, "$ne": []}
        })
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNodeOSMsInSegmentbyCoorDAL(a,b):
    try:
        client = TrafficMongoClient()
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
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNodeOSMByIDDAL(id):
    try:
        client = TrafficMongoClient()
        table = client.db["nodes"]
        print(type(id))
        res = table.find_one({"type": "node","id": id})
        print(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateNodeOSMDAL(body):
    try:
        client = TrafficMongoClient()
        nodeOSMTable = client.db["nodes"]
        body = nodeOSMTable.update_one({'id': body['id']}, {"$set": body})
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findNodesInBBoxDAL(lon_min, lat_min, lon_max, lat_max):
    try:
        client = TrafficMongoClient()
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
    finally:
        client.close()

def findNodesOSMByIDsDAL(ids: list[int]):
    try:
        client = TrafficMongoClient()
        nodeOSMTable = client.db["nodes"]
        cursor = nodeOSMTable.find(
            {"id": {"$in": ids}},
            {"id": 1, "location.coordinates": 1}
        )
        res = list(cursor)
        print(res)
        return res
    except PyMongoError as e:
        raise e