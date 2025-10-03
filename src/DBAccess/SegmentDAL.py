from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify, current_app

def findAllSegmentDAL():
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
        res = segmentTable.find()
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def findSegmentByIDDAL(id):
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
        res = segmentTable.find_one({"id": id})
        return res
    except PyMongoError as e:
        raise e

def findSegmentsByIDsDAL(segment_ids: list):
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
        cursor = segmentTable.find(
            {"id": {"$in": segment_ids}}, 
            {"tags.name": 1, "tags.ref": 1, "id": 1}
        )
        segments = {}
        for seg in cursor:
            seg_id = str(seg.get("id"))
            tags = seg.get("tags", {})
            segments[seg_id] = {
                "name": tags.get("name"),
                "ref": tags.get("ref")
            }
        return segments
    except PyMongoError as e:
        raise e

def findSegmentByNodeDAL(nodeID):
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
        res = segmentTable.find({"nodes": nodeID})
        res = list(res)
        return res
    except PyMongoError as e:
        raise e

def updateSegmentDAL(body):
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
        res = findSegmentByIDDAL(body['id'])
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        print(body)
        segmentTable.update_one({'id': body['id']}, {"$set": body})
        print(body)
        return body
    except PyMongoError as e:
        raise e

def findSegmentsWithNodeIDs(node_ids):
    try:
        client = current_app.config['DB_CLIENT']
        segmentTable = client.db["segments"]
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
        segments = list(segmentTable.aggregate(pipeline))
        return segments
    except PyMongoError as e:
        raise e