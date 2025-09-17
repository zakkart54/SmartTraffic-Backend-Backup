from flask import Blueprint, request, jsonify
from Services.ReportServices import *
from Services.UserServices import checkAdmin, checkToken
from Services.DataServices import deleteData, handleEvaluate
from Services.TrafficStatusInfoServices import insertTrafficStatusInfo, updateTrafficStatusInfo
from pymongo.errors import PyMongoError
import time
report_blueprint = Blueprint('report',__name__)

#Res gọi bằng Service đều trả không cần tuple, nếu phát sinh lỗi thì trả tuple hết.

@report_blueprint.before_request
def reportBeforeRequest():
    #Check Access Token
    access_token = request.headers.get('Authorization')
    if not access_token:
        return 'No access token in header', 401
    try:
        checkToken(access_token)
    except Exception as e:
        print(e)
        return str(e), 401
    
# "TrafficStatusID", "velocity"
@report_blueprint.get('/')
def getAllReport():
    try:
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllReport()
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500
    
@report_blueprint.get('/notQualified')
def getAllUnqualifiedReport():
    try:
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllUnqualifiedReport()
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500

@report_blueprint.get('/<id>')
def getReportID(id):
    try:
        #Tìm uploader:
        res = findReportByID(id)
        uploader = res[0]['uploaderID']
        #Check Token xem có đúng uploader hay admin hay không
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token) or checkToken(access_token)[0] == uploader:
            return res
    except Exception as e:
        print(e)
        return str(e), 500
    

@report_blueprint.get('/uploader/<id>') #New, chưa thêm swagger
def getReportByUploaderID(id):
    try:
        #Check Token xem có đúng uploader hay admin hay không
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token) or checkToken(access_token)[0] == id:
            res = findReportByUploaderID(id)
            return res
        else:
            return 'Forbidden', 403
    except Exception as e:
        print(e)
        return str(e), 500


# "uploaderID": {"bsonType": "objectId"},
# "textID": {"bsonType": "objectId"},
# "imageID": {"bsonType": "objectId"},
# "eval": {"bsonType": "float"},
# "qualified": {"bsonType": "bool"},
# "createdDate": {"bsonType": "date"}
@report_blueprint.post('/')
def insertReportInstance():
    try:
        # ["uploaderID", "textID", "imageID", "eval", "qualified", "createdDate"]
        report = request.get_json()

        #Kiểm tra sự tồn tại của body
        if ("dataImgID" not in report and "dataTextID" not in report) or "lat" not in report or 'lon' not in report:
            return jsonify({"error": "Bad Requestt"}), 400
        print(report)
        #Trường Required
        if 'uploaderID' not in report:
            print('d')
            access_token = request.headers.get('Authorization')
            print(access_token)
            if not access_token: return jsonify({"error": "Bad Request"}), 400 
            uploaderID = checkToken(access_token)[0]
            report['uploaderID'] = uploaderID
        
        if len(report["uploaderID"])!=24:
            return jsonify({"error": "length < 24"}), 400

        #Đảm bảo các trường có đúng không
        for key in report.keys():
            if key not in ["uploaderID", "dataTextID", "dataImgID", "eval", "qualified", "createdDate","lat", "lon"]:
                return jsonify({"error": "Wrong key provided"}), 400 
        
        res = insertReport(report)
        return res
    except Exception as e:
        print(e)
        return str(e), 500

@report_blueprint.put('/')
def changeReportInstance():
    try:
        print('abc')
        report = request.get_json()

        
        #Kiểm tra sự tồn tại của body
        if not report:
            return jsonify({"error": "Bad Request"}), 400
        
        if ("dataImgID" not in report and "dataTextID" not in report) or "segmentID" not in report:
            return jsonify({"error": "Bad Request"}), 400

        if 'uploaderID' not in report:
            access_token = request.headers.get('Authorization')
            if not access_token: return jsonify({"error": "Bad Request"}), 400 
            uploaderID = checkToken(access_token)[0]
            report['uploaderID'] = uploaderID


        #Đảm bảo các trường có đúng không
        for key in report.keys():
            if key not in ["uploaderID", "dataTextID", "dataImgID", "eval", "qualified", "createdDate", "segmentID", "_id"]:
                return jsonify({"error": "Wrong key provided"}), 400

        checkReport = findReportByID(report['_id'])[0]
        if report['uploaderID'] != checkReport['uploaderID']: 
            return jsonify({"error": "uploaderID is different from the original one"}), 400
        res = updateReport(report)
        return res         
    except Exception as e:
        print(e)
        return str(e), 500
    
@report_blueprint.delete('/<id>')
def deleteReportID(id): #Phải xóa image, video kèm theo (nếu có) và xóa luôn status của report đó
    try:
        access_token = request.headers.get('Authorization')
        res = findReportByID(id)
        if res[0]['uploaderID'] != checkToken(access_token)[0] and not checkAdmin(access_token): 
            return 'Forbidden', 403
        if res[0]['dataTextID']:
            deleteData(res[0]['dataTextID'])
        elif res[0]['dataImageID']:
            deleteData(res[0]['dataImageID'])
        res = deleteReport(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    
@report_blueprint.get('/autoVerify/<id>') #Cần thêm swagger
def autoVerifybyID(id):
    try:
        report = findReportByID(id)[0]
        return handleVerify(report)
    except Exception as e:
        print(e)
        return str(e), 500
    
