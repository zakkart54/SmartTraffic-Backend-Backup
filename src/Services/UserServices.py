from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.UserDAL import *
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import bcrypt
from flask_jwt_extended import decode_token
from jwt.exceptions import InvalidTokenError

from flask_jwt_extended import (
    create_access_token, create_refresh_token
)

#Toàn bộ giá trị trả về trong phần Try đều phải trả về bằng tuple (res, statusCode)
#Toàn bộ dữ liệu không phải string thì update lại


def hashPassword(username,password):
    load_dotenv()
    secretKey = os.getenv('SECRET')
    key = hmac.new(secretKey.encode('utf-8'),username.encode('utf-8') + password.encode('utf-8'),hashlib.sha256).digest()
    # print(f'key {key}')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(key,salt)
    return hashed.decode('utf-8')

def checkPassword(username,password,checkhash):
    load_dotenv()
    secretKey = os.getenv('SECRET')
    key = hmac.new(secretKey.encode('utf-8'),username.encode('utf-8') + password.encode('utf-8'),hashlib.sha256).digest()
    return bcrypt.checkpw(key,checkhash.encode('utf-8'))


def checkToken(accessTok):
    try:
        decoded = decode_token(accessTok)  # Tự động xác minh chữ ký và thời gian hết hạn
        print("Token hợp lệ:", decoded)
        id = decoded['sub'] #Lấy identity
        if findUserByID(id)[0]!={}:
            return id, 201
        else:
            raise "Invalid Token!"
    except InvalidTokenError as e:
        print("Token không hợp lệ:", str(e))
        raise e
    
def checkAdmin(accessTok):
    try:
        decoded = decode_token(accessTok)  # Tự động xác minh chữ ký và thời gian hết hạn
        print("Token hợp lệ:", decoded)
        id = decoded['sub'] #Lấy identity
        user = findUserByID(id)[0]
        if user != {}:
            if user['admin']: return True
        else:
            return False
    except InvalidTokenError as e:
        print("Token không hợp lệ:", str(e))
        raise e

def login(body):
    try:
        account = findUserDAL(body)
        if account == None: return 'Invalid Username and Password!', 400
        if checkPassword(body['username'],body['password'],account['password']):
            access_token = create_access_token(identity=str(account["_id"]))
            refresh_token = create_refresh_token(identity=str(account["_id"]))
            createRefreshTokenDAL(account,refresh_token)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return 'Invalid Username and Password!', 400
    except PyMongoError as e:
        raise e
    
def refreshToken(body):
    try:
        refresh_token = findRefreshTokenDAL(body)
        if refresh_token:
            access_token = create_access_token(identity=body["_id"])
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401
    except PyMongoError as e:
        raise e

def findAllUser():
    res = findAllUserDAL()
    for user in res:
        user['_id'] = str(user['_id'])
    return res, 200


def findUserByID(id):
    res = findUserByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    return res, 200

def findUserProfile(id):
    res = findUserByIDDAL(id)
    if res is None:
        return {}, 200
    res_fields = ["username", "phoneNum", "fullName", "email", "DoB"]
    res_data = {field: res.get(field) for field in res_fields}
    return res_data, 200

def findUserByUsername(username):
    res = findUserByUsernameDAL(username)
    if res == None: return {"msg": "Not found"}, 404
    res['_id'] = str(res['_id'])
    return res, 200


def insertUser(body):
    try:
        if 'DoB'  in body: body["DoB"] = datetime.strptime(body["DoB"],"%Y/%m/%d")
        else: body["DoB"] = None
        if 'email' not in body: body['email'] = None
        if 'phoneNum' not in body: body['phoneNum'] = None
        if 'status' not in body: body['status'] = True
        if 'loginType' not in body: body['loginType'] = None
        body["password"] = hashPassword(body["username"],body["password"])
        
        body = insertUserDAL(body)
        
        del body['_id']
        return body, 201
    except PyMongoError as e:
        raise e

def updateUser(body):
    try:
        
        if body['DoB']: body["DoB"] = datetime.strptime(body["DoB"],"%Y/%m/%d")
        body['_id'] = ObjectId(body['_id'])
        body["password"] = hashPassword(body["username"],body["password"])
        res = findUserByIDDAL( body['_id'])
        if res == None: 
            return jsonify({"error": "Not Found"}), 40
        body = updateUserDAL(body)
        del body['_id']
        del body['password']
        return body, 200
    except PyMongoError as e:
        raise e

def deleteUser(id):
    try:
        res = findUserByIDDAL(id)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        deleteUserDAL(id)
        return jsonify({"message": "Successful"}), 200
    except PyMongoError as e:
        raise e
        
def changeUserPassword(user_id, old_password, new_password):
    try:
        res = findUserByIDDAL(user_id)
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        if not checkPassword(res['username'],old_password,res['password']):
            return jsonify({"error": "Password is incorrect"}), 400
        new_hashed = hashPassword(res['username'], new_password)
        res['password'] = new_hashed
        updateUserDAL(res)
        return jsonify({"message": "Successful"}), 200
    except PyMongoError as e:
        raise e