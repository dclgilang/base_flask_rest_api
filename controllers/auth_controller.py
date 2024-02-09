import datetime
from datetime import datetime as timestamp
import traceback
from flask import Blueprint, request, jsonify, render_template
from common.base_response import BaseResponse
from models.employee import Employee
from sqlalchemy.orm import joinedload
from flask_jwt_extended import *
from werkzeug.routing import BaseConverter
from app import db
from repositories.employee_repository import EmployeeRepository
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload

ts = timestamp.utcnow()

AuthBlueprint = Blueprint("Auth", __name__)


@AuthBlueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Invalid request. Make sure to include email and password.'}, 400
    email = data['email']
    password = data['password']
    user = Employee.query.filter_by(email=email).first()
    id = user
    if user:
        if check_password_hash(user.password, password):
            data_user = EmployeeRepository.get_by_email(email)
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(data_user.serialize(), expires_delta=expires)
           
            return jsonify(
            {
                "message": "Login successfully", 
                "status": 200, 
                "data": {
                    "id": data_user.id,
                    "user":  data_user.serialize(),
                    "email": data_user.email,
                    "telepon": data_user.telepon,
                    "usia": data_user.usia,
                    "status_menikah": data_user.status_menikah,
                    "token_access": access_token
                    }
            }
        )
        else:
            return {'message': 'Invalid password'}, 401
    else:
        return {'message': 'Invalid email'}, 401


@AuthBlueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return jsonify(
            {
                "message": "refresh token", 
                "status": 200, 
                "data": {
                    "token": new_token
                    }
            }
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, False)
        return jsonify(response.serialize())


# @AuthBlueprint.route("/password/change", methods=["PUT"])
# @jwt_required()
# def change_password():

#     user_auth = get_jwt_identity()
#     user_id = user_auth["id"]
    
#     json = request.json
#     old_password = json.get("old_password")
#     new_password = json.get("new_password")
#     confirm_password = json.get("confirm_new_password")

#     try:

#         data = UsersRepository.get_by_id(user_id)

#         user_with_roles = (
#         db.session.query(Users, Employee, UserRole, Role)
#         .join(Employee, Users.id == Employee.user_id)
#         .outerjoin(UserRole, Users.id == UserRole.user_id)
#         .outerjoin(Role, UserRole.role_id == Role.id)
#         .filter(Users.id == user_auth["id"])
#         .first()
#          )
#         if user_with_roles:
#             data = user_with_roles.Users
#             employee_data = user_with_roles.Employee
#             role_data = user_with_roles.Role  


#         if data is None :
#             response = BaseResponse(None, "User not found", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400

#         if old_password is None:
#             response = BaseResponse(None, "Old Password is Required", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400

#         checkOldPassword = data.checkPassword(old_password)

#         if checkOldPassword is False :
#             response = BaseResponse(None, "Wrong old password", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400

#         if new_password is None:
#             response = BaseResponse(None, "New Password is Required", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400

#         if old_password == new_password :
#             response = BaseResponse(None, "Old password and New password cannot be the same", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400

#         if new_password != confirm_password :
#             response = BaseResponse(None, "New password or Confirm password is not the same", 0, 0, 0, False)
#             return jsonify(response.serialize()), 400
        
#         data.setPassword(new_password)
#         data.updated_at=ts
#         db.session.commit()

#         LogActivityRepository.create_log(employee_data.nip, employee_data.nama, role_data.name, "Authentication", "Change Password", f"{data.name} melakukan ubah password")
            
#         return (
#             jsonify(
#                 BaseResponse(
#                     "{}".format(data.id),
#                     "Password successfully changed",
#                     1,
#                     1,
#                     1,
#                     True,
#                 ).serialize()
#             ),
#             200,
#         )

#     except Exception as e:
#         response = BaseResponse(None, str(e), 0, 0, 0, False)
#         return jsonify(response.serialize())