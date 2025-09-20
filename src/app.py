from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from Controller.DataController import data_blueprint
from Controller.UserController import user_blueprint
from Controller.NotificationController import notifications_blueprint
from Controller.ImageController import image_blueprint
from Controller.AuthController import auth_blueprint
from Controller.TrafficStatusInfoController import trafficStatusInfo_blueprint
from Controller.NodeOSMController import nodeOSM_blueprint
from Controller.WayOSMController import wayOSM_blueprint
from Controller.RelationOSMController import relationOSM_blueprint
from Controller.SegmentController import segment_blueprint
from Controller.TextController import text_blueprint
from Controller.ReportController import report_blueprint
from EvaluationLib.main import *
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager
)
import os
from dotenv import load_dotenv
from DBConfig.DBConnect import TrafficMongoClient

app = Flask(__name__)

#Connect DB
client = TrafficMongoClient()
app.config['DB_CLIENT'] = client

#Add CORS into app
CORS(app)

#Config JWT
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET')  # Thay bằng khóa bí mật mạnh
app.config['JWT_SECRET_KEY'] = os.getenv('JWTSECRET')  # Khóa riêng cho JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('MAXACCESSTOKENHOURS')))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('MAXREFRESHTOKENDAYS')))

jwt = JWTManager(app)                           

#Swagger Config
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"  # Your OpenAPI JSON file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Sample API 2"},
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#Get Controllers
app.register_blueprint(data_blueprint,url_prefix='/data')
app.register_blueprint(user_blueprint,url_prefix='/user')
app.register_blueprint(notifications_blueprint,url_prefix='/notifications')
app.register_blueprint(text_blueprint,url_prefix='/text')
app.register_blueprint(image_blueprint,url_prefix='/image')
app.register_blueprint(auth_blueprint,url_prefix='/auth')
app.register_blueprint(trafficStatusInfo_blueprint,url_prefix='/trafficStatusInfo')
app.register_blueprint(nodeOSM_blueprint,url_prefix='/nodeOSM')
app.register_blueprint(wayOSM_blueprint,url_prefix='/wayOSM')
app.register_blueprint(relationOSM_blueprint,url_prefix='/relationOSM')
app.register_blueprint(segment_blueprint,url_prefix='/segment')
app.register_blueprint(report_blueprint,url_prefix='/report')

def createDirs():
    base_dir = "storage"

# Create the main directory
    os.makedirs(base_dir, exist_ok=True)
    # Create subdirectories under storage
    subdirs = [
        # Images directories
        "images",
        "images/unverified",
        
        # Images - v_test
        "images/v_test/flooded/positive",
        "images/v_test/flooded/negative",
        "images/v_test/obstacles/positive", 
        "images/v_test/obstacles/negative",
        "images/v_test/police/positive",
        "images/v_test/police/negative",
        "images/v_test/trafficJam/positive",
        "images/v_test/trafficJam/negative",
        
        # Images - v_train
        "images/v_train/flooded/positive",
        "images/v_train/flooded/negative",
        "images/v_train/obstacles/positive",
        "images/v_train/obstacles/negative",
        "images/v_train/police/positive",
        "images/v_train/police/negative",
        "images/v_train/trafficJam/positive",
        "images/v_train/trafficJam/negative",
        
        # Images - v_val
        "images/v_val/flooded/positive",
        "images/v_val/flooded/negative",
        "images/v_val/obstacles/positive",
        "images/v_val/obstacles/negative",
        "images/v_val/police/positive",
        "images/v_val/police/negative",
        "images/v_val/trafficJam/positive",
        "images/v_val/trafficJam/negative",
        
        # Texts directories
        "texts",
        "texts/unverified",
        
        # Texts - v_test
        "texts/v_test/flooded/positive",
        "texts/v_test/flooded/negative",
        "texts/v_test/obstacles/positive",
        "texts/v_test/obstacles/negative",
        "texts/v_test/police/positive",
        "texts/v_test/police/negative",
        "texts/v_test/trafficJam/positive",
        "texts/v_test/trafficJam/negative",
        
        # Texts - v_train
        "texts/v_train/flooded/positive",
        "texts/v_train/flooded/negative",
        "texts/v_train/obstacles/positive",
        "texts/v_train/obstacles/negative",
        "texts/v_train/police/positive",
        "texts/v_train/police/negative",
        "texts/v_train/trafficJam/positive",
        "texts/v_train/trafficJam/negative",
        
        # Texts - v_val
        "texts/v_val/flooded/positive",
        "texts/v_val/flooded/negative",
        "texts/v_val/obstacles/positive",
        "texts/v_val/obstacles/negative",
        "texts/v_val/police/positive",
        "texts/v_val/police/negative",
        "texts/v_val/trafficJam/positive",
        "texts/v_val/trafficJam/negative"
    ]
    # Create each subdirectory
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)
if __name__ == "__main__":
    if not os.path.exists(os.getenv('STORAGE')): createDirs()
    else: print('storage exists')
    app.run() 
