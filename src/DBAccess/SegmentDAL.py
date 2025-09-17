from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from DBConfig.DBConnect import TrafficMongoClient
from flask import jsonify

def findAllSegmentDAL():
    try:
        client = TrafficMongoClient()
        segmentTable = client.db["segments"]
        res = segmentTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findSegmentByIDDAL(id):
    try:
        client = TrafficMongoClient()
        segmentTable = client.db["segments"]
        res = segmentTable.find_one({"id": id})
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findSegmentByNodeDAL(nodeID):
    try:
        client = TrafficMongoClient()
        segmentTable = client.db["segments"]
        res = segmentTable.find({"nodes": nodeID})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def updateSegmentDAL(body):
    try:
        res = findSegmentByIDDAL(body['id'])
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        client = TrafficMongoClient()
        segmentTable = client.db["segments"]
        print(body)
        segmentTable.update_one({'id': body['id']}, {"$set": body})
        print(body)
        return body
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def findSegmentsWithNodeIDs(node_ids):
    try:
        pipeline = [
            {
                "$match": {
                    "nodes": {"$in": node_ids}
                }
            },
            {
                "$lookup": {
                    "from": "statusInfos",
                    "localField": "status",
                    "foreignField": "_id",
                    "as": "status_docs"
                }
            }
        ]
        client = TrafficMongoClient()
        segmentTable = client.db["segments"]
        segments = list(segmentTable.aggregate(pipeline))
        return segments
    except PyMongoError as e:
        raise e
    finally:
        client.close()