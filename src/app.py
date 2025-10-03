from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .Controller.DataController import data_blueprint
from .Controller.UserController import user_blueprint
from .Controller.NotificationController import notifications_blueprint
from .Controller.ImageController import image_blueprint
from .Controller.AuthController import auth_blueprint
from .Controller.TrafficStatusInfoController import trafficStatusInfo_blueprint
from .Controller.NodeOSMController import nodeOSM_blueprint
from .Controller.WayOSMController import wayOSM_blueprint
from .Controller.RelationOSMController import relationOSM_blueprint
from .Controller.SegmentController import segment_blueprint
from .Controller.TextController import text_blueprint
from .Controller.ReportController import report_blueprint
import os
from .EvaluationLib.main import *
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager
)
import os
from dotenv import load_dotenv
from .DBConfig.DBConnect import TrafficMongoClient

app = Flask(__name__)

#Connect DB
app.config['DB_CLIENT'] = TrafficMongoClient()

#Add CORS into app
CORS(app, supports_credentials=True)

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

@app.get('/healthcheck')
def healthcheck():
    return ('Ok', 200)

if __name__ == "__main__":
    client = TrafficMongoClient()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
