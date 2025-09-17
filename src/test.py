
from DBConfig.DBConnect import TrafficMongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
data = {
  "segmentID": "Abc",
  "uploaderID": "123412341234123412341234",
  "type": "text",
  "location": "string"
}

client = TrafficMongoClient()
dataTable = client.db["nodes"]
res = dataTable.find_one({"type": "node","id": 366368130})
print(res)
