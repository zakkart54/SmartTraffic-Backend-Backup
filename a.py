from src.app import *

if __name__ == "__main__":
    client = TrafficMongoClient()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)

# from flask import Flask
# from flask import Blueprint, request, jsonify
# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello():
#     limit = request.args.get('limit',type=int)
#     offset = request.args.get('offset',type=int)
#     return [limit,offset], 200

# if __name__ == '__main__':
#     app.run(debug=True)