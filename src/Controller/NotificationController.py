from flask import Blueprint, request, jsonify
from Services.NotificationServices import *
from Services.UserServices import checkToken
from pymongo.errors import PyMongoError
from bson import ObjectId
notifications_blueprint = Blueprint('notifications',__name__)

#Res gọi bằng Service đều trả không cần tuple, nếu phát sinh lỗi thì trả tuple hết.
#Insert bằng kiểu khác string đều phải thực hiện bước convert hết.

@notifications_blueprint.before_request
def notificationsBeforeRequest():
    print("before notifications")

@notifications_blueprint.get('/')
def getAllNotifications():
    try:
        res = findAllNotifications()
        return res
    except Exception as e:
        print(e)
        return str(e), 500
@notifications_blueprint.get('/<id>')
def getNotificationsID(id):
    try:
        res = findNotificationsByID(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500

@notifications_blueprint.post('/')
def insertNotificationsInstance():
    try:
        notifications = request.get_json()
        #Kiểm tra sự tồn tại của body
        if not notifications:
            return jsonify({"error": "Bad Request"}), 400
        
        #Trường Required
        if 'userID' not in notifications or 'type' not in notifications or 'content' not in notifications:
            return jsonify({"error": "Missing Required Values"}), 400 
        
        #Đảm bảo các trường có đúng không
        for key in notifications.keys():
            if key not in ["userID","type","content"]:
                return jsonify({"error": "Wrong key provided"}), 400 
        res = insertNotifications(notifications)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    
@notifications_blueprint.put('/')
def changeNotificationsInstance():
    try:
        print('abc')
        notifications = request.get_json()

        #Kiểm tra sự tồn tại của body
        if not notifications:
            return jsonify({"error": "Bad Request"}), 400
        
        print(len(notifications["_id"]))
        if len(notifications["_id"])!=24:
            return jsonify({"error": "Bad Request"}), 400
        
        #Đảm bảo các trường có đúng không
        for key in notifications.keys():
            if key not in ["userID","type","content","_id",'segmentID','timeStamp','read']:
                return jsonify({"error": "Wrong key provided"}), 400 
            

        res = updateNotifications(notifications)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    
@notifications_blueprint.delete('/<id>')
def deleteNotificationsID(id):
    try:
        print(len(id))
        if len(id)!=24:
            return jsonify({"error": "Bad Request"}), 400
        res = deleteNotifications(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500
    
@notifications_blueprint.post('/gps')
def createNotificationUsingGPS():
    try:
        body = request.get_json()
        if 'lon' not in body or 'lat' not in body:
            return jsonify({"error": "lat or lon not in body"}), 400
        if 'targetID' not in body:
            access_token = request.headers.get('Authorization')
            if not access_token: return [], 200
            uploaderID = checkToken(access_token)[0]
            body['targetID'] = uploaderID
        return handleNotificationUsingGPS(body['lon'], body['lat'], body['targetID'])
    except Exception as e:
        print(e)
        return str(e), 500
    
@notifications_blueprint.get('/user')
def getNotificationsByUserID():
    try:
        access_token = request.headers.get("Authorization")
        if not access_token: return jsonify({"error": "Bad Request"}), 400 
        id = checkToken(access_token)[0]
        res = findNotificationsByUserID(id)
        return res
    except Exception as e:
        print(e)
        return str(e), 500