from src.app import *

if __name__ == "__main__":
    client = TrafficMongoClient()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
    # findReportByGPS500()

# from flask import Flask
# from flask import Blueprint, request, jsonify
# app = Flask(__name__)

# # @app.route('/', methods=['GET'])
# # def hello():
# #     limit = request.args.get('limit',type=int)
# #     offset = request.args.get('offset',type=int)
# #     return [limit,offset], 200

# # if __name__ == '__main__':
# #     app.run(debug=True)

# client = TrafficMongoClient()
# from pymongo.errors import PyMongoError
# from bson import ObjectId

# def findMax100VerifiedReport():
#     res = findMax100VerifiedReportDAL()
#     for report in res:
#         report['_id'] = str(report['_id'])
#         if report['uploaderID']: report['uploaderID'] = str(report['uploaderID'])
#         if report['dataTextID']: report['dataTextID'] = str(report['dataTextID'])
#         if report['dataImgID']: report['dataImgID'] = str(report['dataImgID'])
#         if report['statusID']: report['statusID'] = str(report['statusID'])
#         report['segmentID'] = str(report['segmentID'])
#     return res, 200

# def findMax100VerifiedReportDAL():
#     try:
#         reportTable = client.db["reports"]
#         res = reportTable.find({"qualified": True}).sort('createdDate', -1).limit(100)
#         res = list(res)
#         return res
#     except PyMongoError as e:
#         raise e

# def findTrafficStatusInfoByID(id):
#     res = findTrafficStatusInfoByIDDAL(id)
#     if res == None: return {}, 200
#     res['_id'] = str(res['_id'])
#     return res, 200

# def findTrafficStatusInfoByIDDAL(id):
#     try:
#         trafficStatusInfoTable = client.db["statusInfos"]
#         res = trafficStatusInfoTable.find_one({"_id": ObjectId(id)})
#         return res
#     except PyMongoError as e:
#         raise e

# def updateSegmentStatus(id):
#     def booltoint(a): return 1 if a else 0
#     def floattobool(a): return True if a>0.5 else False
#     try:
            
#         segmentTable = client.db['segments']
#         segment = segmentTable.find_one({"id": id})
#         # reports = findMax100VerifiedReport()[0]
#         StatusArr = []
#         StatusTable = []
#         for i in range(24): StatusArr.append({
#             'FLOOD': 0,
#             'JAM': 0,
#             'POLICE': 1,
#             'OBSTACLE': 0
#         })
#         # reportLen = len(reports)
#         # for i in reports:
#         #     time = i['createdDate'].hour
#         #     status = findTrafficStatusInfoByID(i['statusID'])[0]
#         #     StatusArr[time]['FLOOD'] += booltoint(status['statuses']['FloodedFlag'])/reportLen
#         #     StatusArr[time]['JAM'] += booltoint(status['statuses']['TrafficJamFlag'])/reportLen
#         #     StatusArr[time]['POLICE'] += booltoint(status['statuses']['PoliceFlag'])/reportLen
#         #     StatusArr[time]['OBSTACLE'] += booltoint(status['statuses']['ObstaclesFlag'])/reportLen
            
#         # print(StatusArr[time]['FLOOD'])
#         # print(StatusArr[time]['JAM'])
#         # print(StatusArr[time]['POLICE'])
#         # print(StatusArr[time]['OBSTACLE'])
#         for i in range(24):
#             StatusTable.append(
#                 {
#                     'FLOOD': floattobool(StatusArr[i]['FLOOD']),
#                     'JAM': floattobool(StatusArr[i]['JAM']),
#                     'POLICE': floattobool(StatusArr[i]['POLICE']),
#                     'OBSTACLE': floattobool(StatusArr[i]['OBSTACLE'])
#                 }
#             )
#         segment['status'] = StatusTable
#         segmentTable.update_one({'id': id}, {"$set": {'status': StatusTable}})
#         return StatusTable, 201
#     except PyMongoError as e:
#         raise e
#     finally:
#         client.close()


# print(updateSegmentStatus("260779470_0"))

from datetime import datetime
print(datetime.now())