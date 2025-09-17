from DBConfig.DBConnect import TrafficMongoClient
from DBAccess.DataDAL import findDataByIDDAL, updateDataDAL
from DBAccess.ImageDAL import *
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from flask import jsonify
from datetime import datetime
import time
import os

def findAllImage():
    res = findAllImagesDAL()
    for image in res:
        image['_id'] = str(image['_id'])
        image['dataID'] = str(image['dataID'])
    print(res)
    return res, 200



def findImageByID(id):
    res = findImageByIDDAL(id)
    if res == None: return {}, 200
    res['_id'] = str(res['_id'])
    res['dataID'] = str(res['dataID'])
    return res, 200
    

def findImageByDataIDList(idlist):
    res = findImageByDataIDListDAL(idlist)
    if res == None: return {}, 200
    res = list(res)
    for img in res:
        img['_id'] = str(img['_id'])
        img['dataID'] = str(img['dataID'])
    return res, 200
def insertImage(body):
    body['dataID'] = ObjectId(body['dataID'])
    
    body = insertImageDAL(body)

    body['_id'] = str(body['_id'])
    body['dataID'] = str(body['dataID'])
    return body, 201
    
def updateImage(body):
    body['_id'] = ObjectId(body['_id'])
    body['dataID'] = ObjectId(body['dataID'])
    res = findImageByIDDAL(body['_id'])
    if res == None: 
        return jsonify({"error": "Not Found"}), 404
    body = updateImageDAL(body)
    del body['_id']
    body['dataID'] = str(body['dataID'])
    return body, 201
    

def deleteImage(id):
    try:
        client = TrafficMongoClient()
        imageTable = client.db["images"]
        res = imageTable.find_one({"_id": ObjectId(id)})
        if res == None: 
            return jsonify({"error": "Not Found"}), 404
        res = imageTable.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Successful"}), 200
    except PyMongoError as e:
        raise e
    finally:
        client.close()

def handleFormDataforImage(image_upload, dataID):
    imgName = f'{time.time()}' + image_upload.filename 
    source = os.getenv('STORAGE') + '/images/unverified/' + imgName
    #Lấy size
    image_upload.seek(0, os.SEEK_END)
    file_size = image_upload.tell()
    image_upload.seek(0)
    print(file_size)

    #Lấy Content Type
    contentType = image_upload.content_type
    print(contentType)
    image = {
        'dataID' : ObjectId(dataID),
        'source' : imgName,
        'length' : file_size,
        'contentType' : contentType,
        "encoding" : "None"
    }
    print('okokkkkkkkkkkkkkk')
    data = findDataByIDDAL(dataID)
    if data['type'] != 'image': return {'error': 'Wrong Data Type!'}, 400
    print('okokkkkkkkkkkkkkk')
    res = insertImageDAL(image)
    imgID = res['_id']
    res['dataID'] = str(res['dataID'])
    res['_id'] = str(res['_id'])
    data['InfoID'] = imgID
    print('okokkkkkkkkkkkkkk')
    updateDataDAL(data)
    image_upload.save(source)
    return res
