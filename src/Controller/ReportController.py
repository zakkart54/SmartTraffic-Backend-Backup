from flask import Blueprint, request, jsonify, copy_current_request_context
from ..Services.ReportServices import *
from ..Services.DataServices import findImageByID,findTextByID, findDataByID, sendContent
from ..Services.UserServices import checkAdmin, checkToken
from ..Services.DataServices import deleteData, findDataDetail
from ..Services.TrafficStatusInfoServices import insertTrafficStatusInfo, updateTrafficStatusInfo
from ..Services.SegmentServices import handleFindSegmentUsingCoor500
import threading
from pymongo.errors import PyMongoError
import time
report_blueprint = Blueprint('report',__name__)

#Res gọi bằng Service đều trả không cần tuple, nếu phát sinh lỗi thì trả tuple hết.

@report_blueprint.before_request
def reportBeforeRequest():
    if request.method == "OPTIONS":
        return "", 200
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
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllReport(limit,offset)
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500
@report_blueprint.get('/valid')
def getAllvalidReport():
    try:
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllvalidReport(limit,offset)
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500
@report_blueprint.get('/neededValidation')
def getAllneededValidationReport():
    try:
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllneededValidationReport(limit,offset)
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500
@report_blueprint.get('/invalid')
def getAllinvalidReport():
    try:
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllinvalidReport(limit,offset)
            return res
        else:
            return 'Forbidden', 403 
    except Exception as e:
        print(e)
        return str(e), 500
    
@report_blueprint.get('/notQualified')
def getAllUnqualifiedReport():
    try:
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllUnqualifiedReport(limit,offset)
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
    

@report_blueprint.get('/uploader') #New, chưa thêm swagger
def getReportByUploader():
    try:
        #Check Token xem có đúng uploader hay admin hay không
        access_token = request.headers.get('Authorization')
        if not access_token: return jsonify({"error": "Unauthorized"}), 401
        uid =  checkToken(access_token)[0]
        res = findReportByUploaderID(uid)
        return res
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

        #Trường Required
        if 'uploaderID' not in report:
            print('d')
            access_token = request.headers.get('Authorization')
            print(access_token)
            if not access_token: return jsonify({"error": "Unauthorized"}), 401
            uploaderID = checkToken(access_token)[0]
            report['uploaderID'] = uploaderID
        
        if len(report["uploaderID"])!=24:
            return jsonify({"error": "length < 24"}), 400

        #Đảm bảo các trường có đúng không
        for key in report.keys():
            if key not in ["uploaderID", "dataTextID", "dataImgID", "eval", "qualified", "createdDate","lat", "lon"]:
                return jsonify({"error": "Wrong key provided"}), 400 
        
        res = insertReport(report)
        
        @copy_current_request_context
        def runAutoVerifyInternal(id):
            try:
                report = findReportByID(id)[0]
                handleVerify(report)
            except Exception as e:
                print("Auto verify failed:", e)
        
        threading.Thread(target=runAutoVerifyInternal, args=(report["_id"],)).start()
        
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
            if not access_token: return jsonify({"error": "Unauthorized"}), 401
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
        res =  handleVerify(report)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    

@report_blueprint.post('/manualVerify') #Cần thêm swagger
def manualVerify():
    try:
        body = request.get_json()
        report = findReportByID(body['id'])[0]
        return handleManual(report,body)
    except Exception as e:
        print(e)
        return str(e), 500
    
@report_blueprint.get('detail/<id>')
def getReportDetail(id):
    try:
        res = findReportByID(id)
        if not res:
            return jsonify({"error": "Report not found"}), 404
        report = res[0]

        access_token = request.headers.get('Authorization')
        if not access_token or not (checkAdmin(access_token) or checkToken(access_token)[0] == report['uploaderID']):
            return 'Forbidden', 403
        data_detail = findDataDetail(report.get('dataID'))

        result = {"report": report}
        if data_detail:
            result["data_detail"] = data_detail

        return result

    except Exception as e:
        print(e)
        return str(e), 500
    

@report_blueprint.post('gps')
def findReportByGPS500():
    try:
        body = request.get_json()
        segments = handleFindSegmentUsingCoor500(body['lon'],body['lat'])[0]
        print(len(segments))
        res = handleFindReportsBySegments(segments)
        return res
    except Exception as e:
        print(e)
        return str(e), 500