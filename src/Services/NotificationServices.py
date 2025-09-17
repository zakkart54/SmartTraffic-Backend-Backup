from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.NotificationDAL import *
from Services.SegmentServices import handleFindSegmentsUsingCoor
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime


def findAllNotifications():
    res = findAllNotificationsDAL()
    for notification in res:
        notification['_id'] = str(notification['_id'])
        notification['userID'] = str(notification['userID'])
    return res, 200


def findNotificationsByID(id):
    res = findNotificationsByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    res['userID'] = str(res['userID'])
    return res, 200
    

def findNotificationsByContent(content):
    res = findNotificationsByContentDAL(content)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    res['userID'] = str(res['userID'])
    return res, 200

def insertNotifications(body):
    objIDList = []
    strUserIDList = body['userID']
    for i in strUserIDList:
        objIDList.append(ObjectId(i))
    body['userID'] = objIDList
    body['createdDate'] = datetime.now()
    
    body = insertNotificationsDAL(body)

    del body['_id']
    body['userID'] = strUserIDList
    return body, 201
def updateNotifications(body):
    objIDList = []
    strUserIDList = body['userID']
    for i in strUserIDList:
        objIDList.append(ObjectId(i))
    body['userID'] = objIDList
    body['_id'] = ObjectId(body['_id'])
    res = findNotificationsByIDDAL(body['_id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    
    body = updateNotificationsDAL(body)

    del body['_id']
    body['userID'] = strUserIDList
    return body, 201

def deleteNotifications(id):
    res = findNotificationsByIDDAL(id)
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    deleteNotificationsDAL(id)
    return jsonify({"message": "Succesful"}), 200

def handleNotificationUsingGPS(lon,lat,uid):
    allNoti = []
    blankStatus = {
        "FLOOD": False,
        "JAM": False,
        "POLICE": False,
        "OBSTACLE": False
    }
    currHour = datetime.now().hour
    segs = handleFindSegmentsUsingCoor(lon,lat)[0]
    for i in segs:
        NotiContent = 'Hiện nay ở đoạn đường '
        status = i['status'][currHour]
        if status != blankStatus:
            print('true')
            textAdded = [
                ' Có ngập' if status['FLOOD'] else '',
                ' Có tắc đường' if status['JAM'] else '',
                ' Có công an' if status['POLICE'] else '',
                ' Có vật cản' if status['OBSTACLE'] else ''
            ]
            NotiContent += i['tags']['name']
            NotiContent += ' với ID là ' + str(i['id'])
            for i in textAdded:
                NotiContent += i
            bodyNoti = {
                'userID': [uid],
                'type': 'STATUS',
                'content': NotiContent,
                'segmentID': str(i['id']),
                'timeStamp': datetime.now(),
                'read': False
            }
            print(bodyNoti)
            noti = insertNotifications(bodyNoti)[0]
            allNoti.append(noti)
    return allNoti, 200

def findNotificationsByUserID(id):
    res = findNotificationsByUserIDDAL(id)
    for noti in res:     
        noti['_id'] = str(noti['_id'])
        noti['userID'] = str(noti['userID'])
    return res, 200