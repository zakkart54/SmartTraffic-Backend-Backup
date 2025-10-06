from ..DBConfig.DBConnect import TrafficMongoClient
from ..DBAccess.DataDAL import *
from ..Services.ImageServices import insertImage, findImageByID, handleFormDataforImage
from ..Services.TextServices import insertText, findTextByID
from ..Services.TrafficStatusInfoServices import findTrafficStatusInfoByID
from ..Services.TrafficStatusInfoServices import updateTrafficStatusInfo, insertTrafficStatusInfo
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify
import os
import time
import shutil
from zoneinfo import ZoneInfo
from dotenv import *
from ..EvaluationLib.main import *
from ..EvaluationLib.image.lib.AITest import *
from ..EvaluationLib.text.lib.AITest import *
import base64
#Toàn bộ giá trị trả về trong phần Try đều phải trả về bằng tuple (res, statusCode)
#Toàn bộ dữ liệu không phải string thì update lại


def findAllData(limit=None,offset=None):
    res, total = findAllDataDAL(limit,offset)
    for data in res:
        data['_id'] = str(data['_id'])
        data['uploaderID'] = str(data['uploaderID'])
        if data['InfoID']is not None: data['InfoID'] = str(data['InfoID'])
        if data['statusID']is not None: data['statusID'] = str(data['statusID'])
        if data['reportID'] is not None: data['reportID'] = str(data['reportID'])
    return {"total": total, "data": res}, 200

def findAllImgData(limit=None,offset=None):
    res, total = findAllImgDataDAL(limit,offset)
    for data in res:
        data['_id'] = str(data['_id'])
        data['uploaderID'] = str(data['uploaderID'])
        if data['InfoID']is not None: data['InfoID'] = str(data['InfoID'])
        if data['statusID']is not None: data['statusID'] = str(data['statusID'])
        if data['reportID'] is not None: data['reportID'] = str(data['reportID'])
    return {"total": total, "data": res}, 200

def findAllTextData(limit=None,offset=None):
    res, total = findAllTextDataDAL(limit,offset)
    for data in res:
        data['_id'] = str(data['_id'])
        data['uploaderID'] = str(data['uploaderID'])
        if data['InfoID']is not None: data['InfoID'] = str(data['InfoID'])
        if data['statusID']is not None: data['statusID'] = str(data['statusID'])
        if data['reportID'] is not None: data['reportID'] = str(data['reportID'])
    return {"total": total, "data": res}, 200

def findDataByID(id):
    res = findDataByIDDAL(id)
    if res is None: return {}, 200
    res['_id'] = str(res['_id'])
    res['uploaderID'] = str(res['uploaderID'])
    if res['InfoID'] is not None: res['InfoID'] = str(res['InfoID'])
    if res['statusID'] is not None: res['statusID'] = str(res['statusID'])
    if res['reportID'] is not None: res['reportID'] = str(res['reportID'])
    return res, 200

def findDataByUploaderID(id):
    res = findDataByUploaderIDDAL(id)
    if res is None: return {}, 200
    res= list(res)
    for data in res:
        data['_id'] = str(data['_id'])
        data['uploaderID'] = str(data['uploaderID'])
        if data['InfoID']is not None: data['InfoID'] = str(data['InfoID'])
        if data['statusID']is not None: data['statusID'] = str(data['statusID'])
    return res, 200
    
def findDataByStatusInfoID(id):
    res = findDataByStatusInfoIDDAL(id)
    if res is None: return {}, 200
    res['_id'] = str(res['_id'])
    res['uploaderID'] = str(res['uploaderID'])
    if res['InfoID'] is not None: res['InfoID'] = str(res['InfoID'])
    if res['statusID'] is not None: res['statusID'] = str(res['statusID'])
    if res['reportID'] is not None: res['reportID'] = str(res['reportID'])
    return res, 200

def findDataByImageID(id):
    res = findDataByImageIDDAL(id)

    print(res)

    if res is None: return {}, 200

    

    res['_id'] = str(res['_id'])
    res['uploaderID'] = str(res['uploaderID'])
    if res['InfoID'] is not None: res['InfoID'] = str(res['InfoID'])
    if res['statusID'] is not None: res['statusID'] = str(res['statusID'])
    if res['reportID'] is not None: res['reportID'] = str(res['reportID'])
    
    return res, 200
def findDataByTextID(id):
    res = findDataByTextIDDAL(id)
    if res is None: return {}, 200
    res['_id'] = str(res['_id'])
    res['uploaderID'] = str(res['uploaderID'])
    if res['InfoID']is not None: res['InfoID'] = str(res['InfoID'])
    if res['statusID']is not None: res['statusID'] = str(res['statusID'])
    return res, 200
def insertData(body):
    body['uploaderID'] = ObjectId(body['uploaderID'])
    if 'InfoID' not in body: body['InfoID'] = None
    else: body['InfoID'] = ObjectId(body['InfoID'])
    if 'reportID' not in body: body['reportID'] = None 
    else: body['reportID'] = ObjectId(body['reportID'])
    if 'uploadTime' not in body: body["uploadTime"] = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
    if 'processed' not in body: body['processed'] = False
    if 'processed_time' not in body: body['processed_time'] = None
    if 'TrainValTest' not in body: body['TrainValTest'] = 0
    if 'location' not in body: body['location'] = None
    if 'statusID' not in body: body['statusID'] = None
    else: body['statusID'] = ObjectId(body['statusID'])
    
    body = insertDataDAL(body)

    body['_id']= str(body['_id'])
    body['uploaderID'] = str(body['uploaderID'])
    if body['InfoID']is not None: body['InfoID'] = str(body['InfoID'])
    if body['reportID']is not None: body['reportID'] = str(body['reportID'])
    if body['statusID']is not None: body['statusID'] = str(body['statusID'])
    return body, 201
def updateData(body):
    body['uploaderID'] = ObjectId(body['uploaderID'])
    print(body['reportID'])
    body['_id'] = ObjectId(body['_id'])
    res = findDataByIDDAL(body['_id'])
    if res is None: 
        return jsonify({"error": "Not Found"}), 404
    print(body['statusID'])
    if 'InfoID' in body: 
        if body['InfoID'] is not None: body['InfoID'] = ObjectId(body['InfoID'])
        else: body['InfoID'] = None
    else: body['InfoID'] = None
    if 'statusID' in body: 
        if body['statusID'] is not None: body['statusID'] = ObjectId(body['statusID'])
        else: body['statusID'] = None
    else: body['statusID'] = None
    if 'reportID' in body:
        if body['reportID'] is not None: body['reportID'] = ObjectId(body['reportID'])
        else: body['reportID'] = None
    else: body['reportID'] = None
    body = updateDataDAL(body)
    body['uploaderID'] = str(body['uploaderID'])
    if body['InfoID']is not None: body['InfoID'] = str(body['InfoID'])
    body['_id'] = str(body['_id'])
    if body['statusID']is not None: body['statusID'] = str(body['statusID'])
    if body['reportID']is not None: body['reportID'] = str(body['reportID'])
    print(body)
    return body, 201

def updateStatus(body):
    body['uploaderID'] = ObjectId(body['uploaderID'])
    body['_id'] = ObjectId(body['_id'])
    res = findDataByIDDAL(body['_id'])
    if res is None: 
        return jsonify({"error": "Not Found"}), 404
    body['statusID'] = ObjectId(body['statusID'])
    body = updateDataDAL(body)
    body['_id'] = str(body['_id'])
    body['uploaderID'] = str(body['uploaderID'])
    return body, 201

def deleteData(id):
    deleteDataDAL(id)
    return jsonify({"message": "Successful"}), 200
    
def findProcessedDataByID(id):
    try:
        client = TrafficMongoClient()
        dataTable = client.db["data"]
        res = dataTable.find({"processed": True})
        if res is None: return {}, 200, 200
        res=list(res)
        for data in res:
            data['_id'] = str(data['_id'])
            data['uploaderID'] = str(data['uploaderID'])
            if data['InfoID']is not None: data['InfoID'] = str(data['InfoID'])
            if data['statusID']is not None: data['statusID'] = str(data['statusID'])
        return res, 200, 200
    except PyMongoError as e:
        raise e
    finally:
        client.close()
    

def handleFormDataImgWithUploaderID(image_upload, bodyUploaderID):
    datajson = {
        'uploaderID' : bodyUploaderID,
        'type' : 'image'
    }
    resData = insertData(datajson)[0]
    resDataID = resData['_id']
    res = handleFormDataforImage(image_upload, resDataID)
    print(res)
    return res, 200



def handleFormDataText(text):
    insertDataJSON = {
        'uploaderID': text['uploaderID'],
        'type': 'text'
    }
    resData = insertData(insertDataJSON)[0]
    resDataID = resData['_id']
    print(resData)
    #["dataID", "source", "length", "contentType", "encoding"]
    #Trường Required
    if 'content' not in text: 
        return jsonify({"error": "Missing Required Values"}), 400 
    #Đảm bảo các trường có đúng không
    for key in text.keys():
        if key not in ["uploaderID", "content"]:
            return jsonify({"error": "Wrong key provided"}), 400 
    
    #Xử lý viết file vào storage
    fileName = f'text_{time.time()}.txt'
    data = findDataByID(resDataID)[0]
    print(f'data {data}')
    if data['type'] != 'text': return {'error': 'Wrong Data Type!'}, 400
    #Đưa vào db
    inputDb = {
        "dataID" : resDataID,
        'source': fileName
    }
    res = insertText(inputDb)
    data['InfoID'] = res[0]['_id']
    updateData(data)
    print(data)
    #Xử lý viết file vào storage
    if res[1]==201:
        source = os.getenv('STORAGE') + '/texts/unverified/' + fileName
        with open(source, 'w', encoding='utf-8') as f:
            f.write(text['content'])
    return res[0], 200

def handleEvaluate(id):
    data = findDataByID(id)[0]
    infoID = str(data['InfoID'])
    if data['type']=='text': print('bbbbbbbbbbbbbbbbbbb')
    data['processed'] = True
    data['processed_time'] = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
    if data['type'] == 'image':
        img = findImageByID(infoID)[0]
        imgSrc = os.getenv('STORAGE') + '/images/unverified/' + img['source']
        policeEval = TestForPolices(imgSrc)
        obstaclesEval = TestForObstacles(imgSrc)
        trafficJamEval = TestForTJam(imgSrc)
        floodedEval = TestForFlooded(imgSrc)
        resEval = policeEval[1] + obstaclesEval[1] + trafficJamEval[1] + floodedEval[1]
        resEval = resEval/4
        # if resEval > 0.8:
        if True:
            data['processed'] = True
            data['processed_time'] = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
            if 'statusID' not in data or data['statusID'] is None:
                status = insertTrafficStatusInfo({
                    'statuses':{
                        'ObstaclesFlag': obstaclesEval[0],
                        'FloodedFlag': floodedEval[0],
                        'PoliceFlag': policeEval[0],
                        'TrafficJamFlag': trafficJamEval[0]
                    }
                })
                data['statusID'] = status[0]['_id']
                updateData(data)
            else:
                status = updateTrafficStatusInfo({
                    '_id': data['statusID'],
                    'statuses':{
                        'ObstaclesFlag': obstaclesEval[0],
                        'FloodedFlag': floodedEval[0],
                        'PoliceFlag': policeEval[0],
                        'TrafficJamFlag': trafficJamEval[0]
                    }
                })
                updateData(data)
        return ({
            "policeEval": 
            {
                "status": policeEval[0],
                "score": float(policeEval[1])
            },
            "obstaclesEval":{
                "status": obstaclesEval[0],
                "score": float(obstaclesEval[1])
            },
            "trafficJamEval": {
                "status": trafficJamEval[0],
                "score": float(trafficJamEval[1])
            },
            "floodedEval": {
                "status": floodedEval[0],
                "score": float(floodedEval[1])
            }}, 200)
    elif data['type'] == 'text':
        print('test text')
        text = findTextByID(infoID)[0]
        textSrc = os.getenv('STORAGE') + '/texts/unverified/' + text['source']
        with open(textSrc, 'r', encoding='utf-8') as file:
            content = file.read()
        overAllEval = NERTest(content)
        #Tự đưa status mới hoặc modify status ID, mới return
        print(data)
        resEval = overAllEval['POLICE']['score'] + overAllEval['OBSTACLE']['score'] + overAllEval['FLOOD']['score'] + overAllEval['JAM']['score']
        resEval = resEval/4
        if True:
            if 'statusID' not in data or data['statusID'] is None:
                status = insertTrafficStatusInfo({
                    'statuses':{
                        'ObstaclesFlag': overAllEval['OBSTACLE']['detected'],
                        'FloodedFlag': overAllEval['FLOOD']['detected'],
                        'PoliceFlag': overAllEval['POLICE']['detected'],
                        'TrafficJamFlag': overAllEval['JAM']['detected']
                    }
                })
                data['statusID'] = status[0]['_id']
                print('textdata1')
                print(data )
                updateData(data)
            else:
                status = updateTrafficStatusInfo({
                    '_id': data['statusID'],
                    'statuses':{
                        'ObstaclesFlag': overAllEval['OBSTACLE']['detected'],
                        'FloodedFlag': overAllEval['FLOOD']['detected'],
                        'PoliceFlag': overAllEval['POLICE']['detected'],
                        'TrafficJamFlag': overAllEval['JAM']['detected']
                    }
                })
                print('textdata2')
                print(data )
                updateData(data)
        return ({
            "policeEval": 
            {
                "status": overAllEval['POLICE']['detected'],
                "score": overAllEval['POLICE']['score'],
            },
            "obstaclesEval":{
                "status": overAllEval['OBSTACLE']['detected'],
                "score": overAllEval['OBSTACLE']['score'],
            },
            "trafficJamEval": {
                "status": overAllEval['JAM']['detected'],
                "score": overAllEval['JAM']['score'],
            },
            "floodedEval": {
                "status": overAllEval['FLOOD']['detected'],
                "score": overAllEval['FLOOD']['score'],
            }}, 200)
    
def handlePutTrainValTest(data, status, value):
    folderOrder = [
        'positive' if status['ObstaclesFlag'] == True else 'negative',
        'positive' if status['FloodedFlag'] == True else 'negative',
        'positive' if status['PoliceFlag'] == True else 'negative',
        'positive' if status['TrafficJamFlag'] == True else 'negative'
    ]
    folders = [
        'obstacles/','flooded/','police/','trafficJam/'
    ]
    image = None
    text = None
    if data['type'] == 'image':
        image = findImageByID(data['InfoID'])[0]
    else: 
        text = findTextByID(data['InfoID'])[0]
    match value:
        case 'train':
            data['TrainValTest'] = 1
            #copy folder
            if data['type'] == 'image':
                for i in range(4):
                    if image is not None: shutil.copy(os.getenv('STORAGE') + '/images/unverified/' + image['source'],os.getenv('STORAGE') + '/images/v_train/' + folders[i] + folderOrder[i])
            else:
                for i in range(4):
                    if text is not None: shutil.copy(os.getenv('STORAGE') + '/texts/unverified/' + text['source'],os.getenv('STORAGE') + '/texts/v_train/' + folders[i] + folderOrder[i])
        case 'val':
            data['TrainValTest'] = 2
            #copy folder
            if data['type'] == 'image':
                for i in range(4):
                    if image is not None: shutil.copy(os.getenv('STORAGE') + '/images/unverified/' + image['source'],os.getenv('STORAGE') + '/images/v_val/' + folders[i] + folderOrder[i])
            else:
                for i in range(4):
                    if text is not None: shutil.copy(os.getenv('STORAGE') + '/texts/unverified/' + text['source'],os.getenv('STORAGE') + '/texts/v_val/' + folders[i] + folderOrder[i])
        case 'test':
            data['TrainValTest'] = 3
            #copy folder
            if data['type'] == 'image':
                for i in range(4):
                    if image is not None: shutil.copy(os.getenv('STORAGE') + '/images/unverified/' + image['source'],os.getenv('STORAGE') + '/images/v_test/' + folders[i] + folderOrder[i])
            else:
                for i in range(4):
                    if text is not None: shutil.copy(os.getenv('STORAGE') + '/texts/unverified/' + text['source'],os.getenv('STORAGE') + '/texts/v_test/' + folders[i] + folderOrder[i])   
    if data['type'] == 'image':
        os.remove(os.getenv('STORAGE') + '/images/unverified/' + image['source'])
    else: 
        os.remove(os.getenv('STORAGE') + '/texts/unverified/' + text['source'])
    updateData(data)
    return data, 200

def sendContent(data):
    storage_root = os.getenv("STORAGE", "storage")
    content = None
    source = None

    if data['type'] == 'image':
        record = findImageByID(data['InfoID'])[0]
        source = record['source']
        base_folder = os.path.join(storage_root, "images")
    else:
        record = findTextByID(data['InfoID'])[0]
        source = record['source']
        base_folder = os.path.join(storage_root, "texts")

    search_folders = [
        os.path.join(base_folder, "unverified"),
        os.path.join(base_folder, "v_train"),
        os.path.join(base_folder, "v_val"),
        os.path.join(base_folder, "v_test"),
    ]

    file_path = None
    for folder in search_folders:
        for root, dirs, files in os.walk(folder):
            if source in files:
                file_path = os.path.join(root, source)
                break
        if file_path:
            break

    if not file_path:
        return {"error": f"File {source} not found"}, 404

    if data['type'] == 'image':
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    return {
        "InfoID": data["InfoID"],
        "type": data["type"],
        "source": source,
        "content": content
    }, 200
    
def findDataDetail(data_id):
    try:
        if not data_id:
            return None
        data_detail = None
        data_records = findDataByID(data_id)
        if data_records:
            data = data_records[0]
            data_detail = {"data": data}

            if data['type'] == 'text' and data.get('InfoID'):
                text_info = findTextByID(data['InfoID'])
                if text_info: 
                    data_detail["text"] = text_info[0]

            elif data['type'] == 'image' and data.get('InfoID'):
                img_info = findImageByID(data['InfoID'])
                if img_info: 
                    data_detail["image"] = img_info[0]

            if data.get('statusID'):
                status_info = findTrafficStatusInfoByID(data['statusID'])
                if status_info:
                    data_detail["status"] = status_info[0]

            file_content, status = sendContent(data)
            if status == 200:
                data_detail["content"] = file_content
            else:
                data_detail["content_error"] = file_content
    except PyMongoError as e:
        raise e