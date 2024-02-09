from flask import Flask, jsonify, send_from_directory
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate
import os
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from common.base_response import BaseResponse
from flask_seeder import FlaskSeeder
from flask_cors import CORS
import mimetypes



app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")

debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

if debug_mode:
    app.config.from_object(DevelopmentConfig())
else:
    app.config.from_object(ProductionConfig())
    

if __name__ == '__main__':
    app.run(debug=debug_mode)


db = SQLAlchemy(app)       
migrate = Migrate(app=app, db=db) 
jwt = JWTManager(app)


seeder = FlaskSeeder(app=app, db=db)
seeder.init_app(app=app, db=db)

from controllers.employee_controllers import EmployeeBlueprint
from controllers.register_controller import RegisterBlueprint
from controllers.auth_controller import AuthBlueprint


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    response = BaseResponse(None, "Token Expired", 0, 0, 0, False)
    return jsonify(response.serialize()), 401


@jwt.unauthorized_loader
def my_unauthorize_callback(jwt_header):
    response = BaseResponse(None, "Unauthorize", 0, 0, 0, False)
    return jsonify(response.serialize()), 401


path_api = "/api/flask/v1"
app.register_blueprint(EmployeeBlueprint, url_prefix=path_api + "/employee")
app.register_blueprint(RegisterBlueprint, url_prefix=path_api + "/register")
app.register_blueprint(AuthBlueprint, url_prefix=path_api + "/auth")



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

FILE_DIR = app.config['UPLOAD_FOLDER']

@app.route(path_api+'/dir_file/<filename>')
def serve_files(filename):
    file_path = os.path.join(FILE_DIR, filename)
    mimetype = mimetypes.guess_type(file_path)[0]
    return send_from_directory(FILE_DIR, filename, mimetype=mimetype)

@app.route(path_api+'/dir_file/<dir>/<filename>')
def serve_cv(dir, filename):
    file_path = os.path.join(FILE_DIR, dir, filename)
    mimetype = mimetypes.guess_type(file_path)[0]
    return send_from_directory(os.path.join(FILE_DIR, dir), filename)