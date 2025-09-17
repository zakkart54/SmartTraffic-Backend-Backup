from flask import Blueprint, request, jsonify
from Services.SegmentServices import *
from pymongo.errors import PyMongoError
import gzip
import json
import base64
segment_blueprint = Blueprint('segment',__name__)

#Res gọi bằng Service đều trả không cần tuple, nếu phát sinh lỗi thì trả tuple hết.

@segment_blueprint.before_request
def segmentBeforeRequest():
    print("before segment")

@segment_blueprint.get('/')
def getAllSegment():
    try:
        res = findAllSegment()
        return res
    except Exception as e:
        print(e)
        return str(e), 500
@segment_blueprint.get('/<id>')
def getSegmentID(id):
    try:
        res = findSegmentByID(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
@segment_blueprint.post('/gps')
def findSegmentUsingCoor():
    try:
        coor = request.get_json()
        return handleFindSegmentUsingCoor(coor['lon'],coor['lat'])
        
    except Exception as e:
        print(e)
        return str(e), 500

@segment_blueprint.put('/')
def changeSegmentInstance():
    try:
        print('abc')
        segment = request.get_json()

        #Kiểm tra sự tồn tại của body
        if not segment:
            return jsonify({"error": "Bad Request"}), 400
        
        #Đảm bảo các trường có đúng không
        for key in segment.keys():
            if key not in ["type","id","way_id","nodes","tags","version","timestamp","changeset","uid","user","status"]:
                return jsonify({"error": "Wrong key provided"}), 400 

        res = updateSegment(segment)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    

@segment_blueprint.post("/map")
def getMapSegment():
    try:
        coor = request.get_json()
        lon_min = coor.get("lon_min")
        lat_min = coor.get("lat_min")
        lon_max = coor.get("lon_max")
        lat_max = coor.get("lat_max")

        if None in [lon_min, lat_min, lon_max, lat_max]:
            return jsonify({"error": "Missing coordinates"}), 400

        segments, status = findSegmentsInBBox(lon_min, lat_min, lon_max, lat_max)
        if status != 200:
            return jsonify({"error": "Service error"}), status

        json_bytes = json.dumps({"data": segments}).encode("utf-8")
        gzipped = gzip.compress(json_bytes)
        b64data = base64.b64encode(gzipped).decode("utf-8")

        return jsonify({"data": b64data}), 200
    except Exception as e:
        print("Error in findSegmentUsingCoor:", e)
        return jsonify({"error": str(e)}), 500