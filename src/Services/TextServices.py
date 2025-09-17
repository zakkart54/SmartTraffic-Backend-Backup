from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime
from DBAccess.TextDAL import *

def findAllText():
    res = findAllTextDAL()
    for text in res:
        text['_id'] = str(text['_id'])
        text['dataID'] = str(text['dataID'])
    return res, 200


def findTextByID(id):
    res = findTextByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    res['dataID'] = str(res['dataID'])
    return res, 200

def findTextByDataIDList(idlist):
    res = findTextByDataIDListDAL(idlist)
    for i in res:
        i['_id'] = str(i['_id'])
        i['dataID'] = str(i['dataID'])
    return res, 200

def insertText(body):
    body['dataID'] = ObjectId(body['dataID'])
    
    body = insertTextDAL(body)

    body['_id'] = str(body['_id'])
    body['dataID'] = str(body['dataID'])
    return body, 201
def updateText(body):
    body['_id'] = ObjectId(body['_id'])
    body['dataID'] = ObjectId(body['dataID'])
    
    res = findTextByIDDAL(body['_id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    body = updateTextDAL(body)
    body['_id'] = str(body['_id'])
    body['dataID'] = str(body['dataID'])
    return body, 201

def deleteText(id):
    res = findTextByIDDAL(id)
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    deleteTextDAL(id)
    return jsonify({"message": "Successful"}), 200