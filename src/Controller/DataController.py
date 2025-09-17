from flask import Blueprint, request, jsonify
from Services.DataServices import *
from Services.UserServices import checkToken,checkAdmin
from Services.ImageServices import findImageByID, insertImage
from Services.ImageServices import deleteImage
from Services.TextServices import deleteText, findTextByID
from Services.ReportServices import findReportByID, updateReport
from Services.TrafficStatusInfoServices import findTrafficStatusInfoByID, deleteTrafficStatusInfo
from pymongo.errors import PyMongoError

data_blueprint = Blueprint('data',__name__)
from dotenv import *
import os
import time
import shutil

#Res gọi bằng Service đều trả không cần tuple, nếu phát sinh lỗi thì trả tuple hết.

@data_blueprint.before_request
def dataBeforeRequest(): #Check token người dùng
    access_token = request.headers.get('Authorization')
    if not access_token:
        return 'No access token in header', 401
    try:
        checkToken(access_token)
    except Exception as e:
        print(e)
        return str(e), 401

@data_blueprint.get('/')
def getAllData():
    try:
        access_token = request.headers.get('Authorization')
        if checkAdmin(access_token):
            res = findAllData()
            return res
        else:
            return 'Forbidden', 403
    except Exception as e:
        print(e)
        return str(e), 500
@data_blueprint.get('/<id>')
def getDataID(id):
    try:
        access_token = request.headers.get('Authorization')
        res = findDataByID(id)
        if res[0]['uploaderID'] != checkToken(access_token)[0] and not checkAdmin(access_token): 
            return 'Forbidden', 403
        return res
    except Exception as e:
        print(e)
        return str(e), 500

@data_blueprint.post('/')
def insertDataInstance():
    try:
        data = request.get_json()
        #Kiểm tra sự tồn tại của body
        if not data:
            return jsonify({"error": "Bad Request"}), 400
        
        #Nếu k có uploaderID, sử dụng check auth.
        if 'uploaderID' not in data:
            access_token = request.headers.get('Authorization')
            if not access_token: return jsonify({"error": "Bad Request"}), 400 
            uploaderID = checkToken(access_token)[0]
            data['uploaderID'] = uploaderID
    
        #Trường Required
        if 'type' not in data or 'segmentID' not in data: 
            return jsonify({"error": "Missing Required Values"}), 400 
        
        #Đảm bảo các trường có đúng không
        for key in data.keys():
            if key not in ["segmentID","uploaderID","type","InfoID","processed","processed_time","TrainValTest","location"]:
                return jsonify({"error": "Wrong key provided"}), 400 
        
        res = insertData(data)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    
@data_blueprint.post('/img')
def insertDataImageInstance():
    try:
        content_type = request.headers.get('Content-Type')
        
        #Phần form-data
        if content_type.startswith('multipart/form-data'):
            image_upload = request.files.get('fileUpload')
            if not image_upload: return jsonify({"error": "No Image inserted"}), 400 
            if request.form.get('uploaderID'): bodyUploaderID = ObjectId(request.form.get('uploaderID'))
            else:
                bodyUploaderID = None
            if not bodyUploaderID:
                access_token = request.headers.get('Authorization')
                if not access_token: return jsonify({"error": "Bad Request"}), 400 
                bodyUploaderID = checkToken(access_token)[0]
            return handleFormDataImgWithUploaderID(image_upload,bodyUploaderID)
        elif content_type == 'application/json':
            image = request.get_json()
            #Kiểm tra sự tồn tại của body
            if not image:
                return jsonify({"error": "Bad Request"}), 400
            if 'uploaderID' not in image:
                access_token = request.headers.get('Authorization')
                if not access_token: return jsonify({"error": "Bad Request"}), 400 
                uploaderID = checkToken(access_token)[0]
                data['uploaderID'] = uploaderID
            #Validation
            #Trường Required
            if 'uploaderID' not in image or 'source' not in image or 'length' not in image or 'contentType' not in image or 'encoding' not in image: 
                return jsonify({"error": "Missing Required Values"}), 400 
            
            #Đảm bảo các trường có đúng không
            for key in image.keys():
                if key not in ["uploaderID", "source", "length", "contentType", "encoding"]:
                    return jsonify({"error": "Wrong key provided"}), 400 
                
            datajson = {
                'uploaderID' : image['uploaderID'],
                'type' : 'image'
            }

            resData = insertData(datajson)[0]
            resDataID = resData['_id']

            imgjson = {
                "dataID" : resDataID, 
                "source" : image['source'], 
                "length" : image['length'], 
                "contentType" : image['contentType'], 
                "encoding" : image['encoding']
            }
            print('abc')
            data = findDataByID(resDataID)[0]
            if data['type'] != 'image': return {'error': 'Wrong Data Type!'}, 400
            res = insertImage(image)
            print('abc')
            imgID = res[0]['_id']
            data['InfoID'] = imgID
            updateData(data)
            return res
    except Exception as e:
        print(e)
        return str(e), 500
    
    
@data_blueprint.post('/text')
def insertDataTextInstance():
    try:
        text = request.get_json()
        #Kiểm tra sự tồn tại của body
        if not text:
            return jsonify({"error": "Bad Request"}), 400
        if 'uploaderID' not in text:
            access_token = request.headers.get('Authorization')
            if not access_token: return jsonify({"error": "Bad Request"}), 400 
            text['uploaderID'] = checkToken(access_token)[0]
        return handleFormDataText(text)
    except Exception as e:
        print(e)
        return str(e), 500    
    
@data_blueprint.put('/')
def changeDataInstance():
    try:
        data = request.get_json()

        #Kiểm tra sự tồn tại của body
        if not data:
            return jsonify({"error": "Bad Request"}), 400
        
        if len(data["_id"])!=24:
            return jsonify({"error": "Bad Request"}), 400
        
        if 'uploaderID' not in data:
            access_token = request.headers.get('Authorization')
            if not access_token: return jsonify({"error": "Bad Request"}), 400 
            uploaderID = checkToken(access_token)[0]
            data['uploaderID'] = uploaderID
            
        #Đảm bảo các trường có đúng không
        for key in data.keys():
            if key not in ["segmentID","type","InfoID","uploadTime","location","_id","statusID","reportID","uploaderID"]:
                return jsonify({"error": "Wrong key provided"}), 400 

        checkData = findDataByID(data['_id'])[0]
        if data['uploaderID'] != checkData['uploaderID']: 
            return jsonify({"error": "uploaderID is different from the original one"}), 400
        res = updateData(data)
        return res         
    except Exception as e:
        print(e)
        return str(e), 500
    
@data_blueprint.delete('/<id>')
def deleteDataID(id): #Phải xóa image, video kèm theo (nếu có) và xóa luôn status của data đó
    try:
        access_token = request.headers.get('Authorization')
        res = findDataByID(id)
        print(res)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        if res[0]['uploaderID'] != checkToken(access_token)[0] and not checkAdmin(access_token): 
            return 'Forbidden', 403
        if res[0]['type'] == 'text':
            deleteText(res[0]['InfoID'])
            if res[0]['reportID'] is not None:
                report = findReportByID(res[0]['reportID'])[0]
                report['dataTextID'] = None
                updateReport(report)
        elif res[0]['type'] == 'image':
            deleteImage(res[0]['InfoID'])
            if res[0]['reportID'] is not None:
                report = findReportByID(res[0]['reportID'])[0]
                report['dataImageID'] = None
                updateReport(report)
        if res[0]['statusID'] is not None: 
            print('2')
            deleteTrafficStatusInfo(res[0]['statusID'])
        res = deleteData(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500

@data_blueprint.get('/eval/<id>')
def evaluateStatus(id):
    try:
        return handleEvaluate(id)
    except Exception as e:
        print(e)
        return str(e), 500

@data_blueprint.put('/manualEvaluate')
def manualEvaluate(): #Gắn status lên data thôi.
    data = request.get_json()

    #Kiểm tra sự tồn tại của body
    if not data:
        return jsonify({"error": "Bad Request"}), 400
    
    print(len(data["_id"]))
    if len(data["_id"])!=24:
        return jsonify({"error": "Bad Request"}), 400
    
    access_token = request.headers.get('Authorization')
    if not access_token: return jsonify({"error": "Bad Request"}), 400 
    if not checkAdmin(access_token)[0]: return jsonify({"error": "Forbidden"}), 403
        
    #Đảm bảo các trường có đúng không
    for key in data.keys():
        if key not in ['ObstaclesFlag','FloodedFlag',' PoliceFlag', 'TrafficJamFlag',"_id"]:
            return jsonify({"error": "Wrong key provided"}), 400 

    res = updateStatus(data)
    return res

@data_blueprint.put('/trainValTest') #Cần thêm swagger
def putTrainValTestValue(): # body: '_id', 'value'
    try:
        load_dotenv()
        #Check Admin
        access_token = request.headers.get('Authorization')
        if not checkAdmin(access_token): 
            return 'Forbidden', 403
        body = request.get_json()
        data = findDataByID(body['_id'])[0]
        if not data['processed']: return 'Data is not verified', 400
        status = findTrafficStatusInfoByID(data['statusID'])[0]
        if not status: return 'Status is not created', 400
        status = status['statuses']
        return handlePutTrainValTest(data, status, body['value'])
    except Exception as e:
        print(e)
        return str(e), 500