from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.ReportDAL import *
from Services.DataServices import handleEvaluate
from Services.TrafficStatusInfoServices import insertTrafficStatusInfo, updateTrafficStatusInfo, findTrafficStatusInfoByID
from Services.SegmentServices import handleFindSegmentUsingCoor
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
from flask import jsonify
client = TrafficMongoClient()

reportTable = client.db["reports"]


def findAllReport():
    res = findAllReportDAL()
    for report in res:
        report['_id'] = str(report['_id'])
        if report['uploaderID']: report['uploaderID'] = str(report['uploaderID'])
        if report['dataTextID']: report['dataTextID'] = str(report['dataTextID'])
        if report['dataImgID']: report['dataImgID'] = str(report['dataImgID'])
        if report['statusID']: report['statusID'] = str(report['statusID'])
        report['segmentID'] = str(report['segmentID'])
    return res, 200

    
def findMax100VerifiedReport():
    res = findMax100VerifiedReportDAL()
    for report in res:
        report['_id'] = str(report['_id'])
        if report['uploaderID']: report['uploaderID'] = str(report['uploaderID'])
        if report['dataTextID']: report['dataTextID'] = str(report['dataTextID'])
        if report['dataImgID']: report['dataImgID'] = str(report['dataImgID'])
        if report['statusID']: report['statusID'] = str(report['statusID'])
        report['segmentID'] = str(report['segmentID'])
    return res, 200

def findAllUnqualifiedReport():
    res = findAllUnqualifiedReportDAL()
    for report in res:
        report['_id'] = str(report['_id'])
        if report['uploaderID']: report['uploaderID'] = str(report['uploaderID'])
        if report['dataTextID']: report['dataTextID'] = str(report['dataTextID'])
        if report['dataImgID']: report['dataImgID'] = str(report['dataImgID'])
        if report['statusID']: report['statusID'] = str(report['statusID'])
        report['segmentID'] = str(report['segmentID'])
    return res, 200

def findReportByID(id):

    res = findReportByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    if res['uploaderID']: res['uploaderID'] = str(res['uploaderID'])
    if res['dataTextID']: res['dataTextID'] = str(res['dataTextID'])
    if res['dataImgID']: res['dataImgID'] = str(res['dataImgID'])
    if res['statusID']: res['statusID'] = str(res['statusID'])
    res['segmentID'] = str(res['segmentID'])
    return res, 200

def findReportByUploaderID(id):
    try:
        res = findReportByUploaderIDDAL(id)
        for report in res:
            report['_id'] = str(report['_id'])
            if report['uploaderID']: report['uploaderID'] = str(report['uploaderID'])
            if report['dataTextID']: report['dataTextID'] = str(report['dataTextID'])
            if report['dataImgID']: report['dataImgID'] = str(report['dataImgID'])
            if report['statusID']: report['statusID'] = str(report['statusID'])
            report['segmentID'] = str(report['segmentID'])
        return res, 200
    except PyMongoError as e:
        raise e
    finally:
        client.close()
    
def findReportByDataImageID(id):
    res = findReportByDataImageIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    if res['uploaderID']: res['uploaderID'] = str(res['uploaderID'])
    if res['dataTextID']: res['dataTextID'] = str(res['dataTextID'])
    if res['dataImgID']: res['dataImgID'] = str(res['dataImgID'])
    if res['statusID']: res['statusID'] = str(res['statusID'])
    res['segmentID'] = str(res['segmentID'])
    return res, 200
    
def findReportDataTextID(id):
    res = findReportDataTextIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    if res['uploaderID']: res['uploaderID'] = str(res['uploaderID'])
    if res['dataTextID']: res['dataTextID'] = str(res['dataTextID'])
    if res['dataImgID']: res['dataImgID'] = str(res['dataImgID'])
    if res['statusID']: res['statusID'] = str(res['statusID'])
    res['segmentID'] = str(res['segmentID'])
    return res, 200


def insertReport(body):
    try:
        print(body)
        body['uploaderID'] = ObjectId(body['uploaderID'])
        if 'dataTextID' not in body: body['dataTextID'] = None
        else: body['dataTextID'] = ObjectId(body['dataTextID'])
        if 'dataImgID' not in body: body['dataImgID'] = None
        else: body['dataImgID'] = ObjectId(body['dataImgID'])
        if 'eval' not in body: body["eval"] = 0.0
        if 'qualified' not in body: body['qualified'] = False
        if 'createdDate' not in body: body['createdDate'] = datetime.today()
        if 'statusID' not in body: body['statusID'] = None
        else: body['statusID'] = ObjectId(body['statusID'])
        body['segmentID'] = handleFindSegmentUsingCoor(body['lon'],body['lat'])[0]['id']
        
        print(body)
        body = insertReportDAL(body)

        body['_id'] = str(body['_id'])
        body['uploaderID'] = str(body['uploaderID'])
        body['segmentID'] = str(body['segmentID'])
        if 'dataTextID' in body: body['dataTextID'] = str(body['dataTextID'])
        if 'dataImgID' in body: body['dataImgID'] = str(body['dataImgID'])
        if 'statusID' in body: body['statusID'] = str(body['statusID'])
        return body, 201
    except PyMongoError as e:
        raise e
    finally:
        client.close()
def updateReport(body):
    try:
        
        body['uploaderID'] = ObjectId(body['uploaderID'])
        body['dataTextID'] = ObjectId(body['dataTextID'])
        body['dataImgID'] = ObjectId(body['dataImgID'])
        if 'statusID' in body: body['statusID'] = ObjectId(body['statusID'])
        body['_id'] = ObjectId(body['_id'])
        res = findReportByIDDAL( body['_id'])
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        
        body = updateReportDAL(body)

        body['_id'] = str(body['_id'])
        if body['uploaderID']: body['uploaderID'] = str(body['uploaderID'])
        if 'dataTextID' in body: body['dataTextID'] = str(body['dataTextID'])
        if 'dataImgID' in body: body['dataImgID'] = str(body['dataImgID'])
        if 'statusID' in body: body['statusID'] = str(body['statusID'])
        body['segmentID'] = str(body['segmentID'])
        return body, 201
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def deleteReport(id):
    try:
        res = findReportByIDDAL(id)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        res = deleteReportDAL(id)
        return jsonify({"message": "Successful"}), 200
    except PyMongoError as e:
        raise e
    finally:
        client.close()
    

def handleVerify(report):
    #Tìm textID và ImgID để tính toán
    text = None
    img = None
    if report['dataTextID'] != None: 
        currTextID = report['dataTextID']
        text = handleEvaluate(currTextID)[0]
    if report['dataImgID'] != None: 
        currImgID = report['dataImgID']
        img = handleEvaluate(currImgID)[0]
    harmony = {}
    fcount = 0
    if text == None and img == None: return jsonify({"error": "No Data included"}), 400
    elif text == None: harmony = img
    elif img == None: harmony = text
    else:
        score = 0
        for k in img.keys():
            if text[k]['status']==img[k]['status']:
                harmony[k] = {
                    "status": text[k]['status'],
                    "score": (text[k]['score']*img[k]['score']*2)/(text[k]['score']+img[k]['score'])
                }
                score += harmony[k]["score"]
            else:
                fcount +=1
                if text[k]['status'] == False:
                    harmony[k] = {
                        "status": False,
                        "score": (text[k]['score']*(1-img[k]['score'])*2)/(text[k]['score']+(1-img[k]['score']))
                    }
                    score += harmony[k]["score"]
                else:
                    harmony[k] = {
                        "status": False,
                        "score": ((1-text[k]['score'])*img[k]['score']*2)/((1-text[k]['score'])+img[k]['score'])
                    }
                    score += harmony[k]["score"]
    resEval = 0
    for k in harmony.keys():
        resEval += harmony[k]["score"]/4
    if fcount < 2 and resEval > 0.8:
        report['qualified'] = True
        report['eval'] = resEval
    #Thêm hoặc cập nhật lại status
    if  not report['statusID'] or report['statusID']==None:
        status = insertTrafficStatusInfo({
            'statuses':{
                'ObstaclesFlag': harmony['obstaclesEval']['status'],
                'FloodedFlag': harmony['floodedEval']['status'],
                'PoliceFlag': harmony['policeEval']['status'],
                'TrafficJamFlag': harmony['trafficJamEval']['status']
            }
        })
        report['statusID'] = status[0]['_id']
        updateReport(report)
    else:
        status = updateTrafficStatusInfo({
            '_id': report['statusID'],
            'statuses':{
                'ObstaclesFlag': harmony['obstaclesEval']['status'],
                'FloodedFlag': harmony['floodedEval']['status'],
                'PoliceFlag': harmony['policeEval']['status'],
                'TrafficJamFlag': harmony['trafficJamEval']['status']
            }
        })
        updateReport(report)
    updateSegmentStatus(report['segmentID'])
    return harmony, 200


def updateSegmentStatus(id):
    def booltoint(a): return 1 if a else 0
    def floattobool(a): return True if a>0.5 else False
    try:
        client = TrafficMongoClient()    
        segmentTable = client.db['segments']
        segment = segmentTable.find_one({"id": id})
        reports = findMax100VerifiedReport()[0]
        StatusArr = []
        StatusTable = []
        for i in range(24): StatusArr.append({
            'FLOOD': 0,
            'JAM': 0,
            'POLICE': 0,
            'OBSTACLE': 0
        })
        reportLen = len(reports)
        for i in reports:
            time = i['createdDate'].hour
            status = findTrafficStatusInfoByID(i['statusID'])[0]
            print(status)
            StatusArr[time]['FLOOD'] += booltoint(status['statuses']['FloodedFlag'])/reportLen
            StatusArr[time]['JAM'] += booltoint(status['statuses']['TrafficJamFlag'])/reportLen
            StatusArr[time]['POLICE'] += booltoint(status['statuses']['PoliceFlag'])/reportLen
            StatusArr[time]['OBSTACLE'] += booltoint(status['statuses']['ObstaclesFlag'])/reportLen
        for i in range(24):
            StatusTable.append(
                {
                    'FLOOD': floattobool(StatusArr[i]['FLOOD']),
                    'JAM': floattobool(StatusArr[i]['JAM']),
                    'POLICE': floattobool(StatusArr[i]['POLICE']),
                    'OBSTACLE': floattobool(StatusArr[i]['OBSTACLE'])
                }
            )
        print(reportLen)
        segment['status'] = StatusTable
        segmentTable.update_one({'id': id}, {"$set": {'status': StatusTable}})
        return StatusTable, 201
    except PyMongoError as e:
        raise e
    finally:
        client.close()