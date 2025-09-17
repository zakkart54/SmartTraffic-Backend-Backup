from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.SegmentDAL import *
from DBAccess.NodeOSMDAL import findNodesInBBoxDAL, findNodesOSMByIDsDAL
from Services.NodeOSMServices import findNodeOSMInSegmentbyCoor, findNodeOSMsInSegmentbyCoor
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
import datetime

#["type","id","way_id","segments","tags","version","timestamp","changeset","uid","user"]:
def findAllSegment():
    res = findAllSegmentDAL()
    for i in res:
        del i['_id']
    return res, 200


def findSegmentByID(id):
    res = findSegmentByIDDAL(id)
    del res['_id']
    if res == None: return {}, 200
    return res, 200
    
def findSegmentByCoor(lon,lat):
    res = findNodeOSMInSegmentbyCoor(lon,lat)[0]
    if res == {}: return {}, 200
    nodeID = res['id']
    res = findSegmentByNodeDAL(nodeID)
    if res == None: return {}, 200
    return list(res), 200

def updateSegment(body):
    res = findSegmentByIDDAL(body['id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    body = updateSegmentDAL(body)
    return body, 201
    

def handleFindSegmentUsingCoor(lon,lat):
    print(lon,lat)
    nearestNode = findNodeOSMInSegmentbyCoor(lon,lat)[0]['id']
    print(nearestNode)
    resSegment = findSegmentByNode(nearestNode)[0]
    return resSegment, 200

def findSegmentByNode(nodeID):
    res = findSegmentByNodeDAL(nodeID)
    for i in res:
        del i['_id']
    return res, 200

def handleFindSegmentsUsingCoor(lon,lat):
    nearestNodes = findNodeOSMsInSegmentbyCoor(lon,lat)[0]
    resSegments = []
    for i in nearestNodes:
        seg = findSegmentByNode(i['id'])[0]
        if seg not in resSegments:
            resSegments.append(seg)
    return resSegments, 200

def findSegmentsInBBox(lon_min, lat_min, lon_max, lat_max):
    try:
        # Lấy node IDs trong bbox
        nodes_in_bbox = findNodesInBBoxDAL(lon_min, lat_min, lon_max, lat_max)
        node_ids = [n["id"] for n in nodes_in_bbox]
        if not node_ids:
            return [], 200
        
        segments = findSegmentsWithNodeIDs(node_ids)

        result = []
        for seg in segments:
            seg_node_ids = [int(n) for n in seg["nodes"]]
            seg_nodes = findNodesOSMByIDsDAL(seg_node_ids)
            for r in seg_nodes:
                r.pop('_id', None)
            seg_node_dict = {n["id"]: n for n in seg_nodes}

            seg_obj = {
                "id": seg["id"],
                "coordinates": [],
                "status": [s.get("statuses", {}) for s in seg.get("status_docs", [])]
            }

            # build coordinates
            for n_ref in seg_node_ids:
                if n_ref in seg_node_dict:
                    coords = seg_node_dict[n_ref]["location"]["coordinates"]
                    seg_obj["coordinates"].append(coords)

            result.append(seg_obj)
        return result, 200
    except PyMongoError as e:
        raise e
