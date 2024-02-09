from flask import Blueprint, request, jsonify
from app import db
import datetime
from common.base_response import BaseResponse
from common.error_response import ErrorResponse
from flask_jwt_extended import *
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository
import traceback 
from flask import send_from_directory
from uuid import UUID
from common.InvalidUUID import InvalidUUIDError

ts = datetime.datetime.utcnow()

EmployeeBlueprint = Blueprint("employee", __name__)    

@EmployeeBlueprint.route("", methods=["GET"])
def employee_list_all():
    if request.method == "GET":
        try:
            filter_value = request.args.get("filter", '')
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            data = EmployeeRepository.get_list(filter_value, page, limit)

            return (
                jsonify(
                    BaseResponse(
                        [e.serialize() for e in data],
                        "Employee successfully showed",
                        page,
                        limit,
                        len(data),
                        True,
                    ).serialize()
                ),
                200,
            )
        except Exception as e:
            response = BaseResponse(None, str(e), 0, 0, 0, False)
            return jsonify(response.serialize())
        
@EmployeeBlueprint.route("/detail/<string:id_user>", methods=["GET"])
def employee_by_id(id_user):
    try:
        data = EmployeeRepository.get_by_id_user(id_user)
        if data is None:
            return ErrorResponse("User not found!", 404).serialize()
        return (
            jsonify(
                BaseResponse(
                    data.serialize(),
                    "Detail User successfully showed",
                    1,
                    1,
                    1,
                    True,
                ).serialize()
            ),
            200,
        )
    except InvalidUUIDError:
        return ErrorResponse("User not found!", 400).serialize()
    except Exception as e:
        response = BaseResponse(None, str(e), 0, 0, 0, False)
        return jsonify(response.serialize())
    

@EmployeeBlueprint.route("/detail/by_nip/<string:nip>", methods=["GET"])
def employee_by_nip(nip):
    try:
        data = EmployeeRepository.get_by_nip(nip)
        if data is None:
            return ErrorResponse("User not found!", 404).serialize()
        return (
            jsonify(
                BaseResponse(
                    data.serialize(),
                    "Detail User successfully showed",
                    1,
                    1,
                    1,
                    True,
                ).serialize()
            ),
            200,
        )
    except InvalidUUIDError:
        return ErrorResponse("User not found!", 400).serialize()
    except Exception as e:
        response = BaseResponse(None, str(e), 0, 0, 0, False)
        return jsonify(response.serialize())
    
@EmployeeBlueprint.route("/delete/<string:id_user>", methods=["DELETE"])
def delete_user(id_user):
    # user_auth = get_jwt_identity()
    if request.method == "DELETE":
        try:
          
            data = EmployeeRepository.get_by_id_user(id_user)
            if data is None:
                return ErrorResponse("User not found!", 404).serialize()
            else:
                data.deleted_id = id_user
                data.deleted_at = datetime.datetime.utcnow()
                db.session.commit()
            return (
                jsonify(
                    BaseResponse(
                        data.serialize(),
                        "User successfully deleted",
                        1,
                        1,
                        1,
                        True,
                    ).serialize()
                ),
                200,
            )
        except Exception as e:
            response = BaseResponse(None, str(e), 0, 0, 0, False)
            return jsonify(response.serialize())