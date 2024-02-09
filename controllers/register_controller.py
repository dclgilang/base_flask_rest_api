import traceback
from flask import Blueprint, request, jsonify, Flask
from app import db
import datetime
from common.base_response import BaseResponse
from models.employee import Employee
from common.base_response import BaseResponse
from common.error_response import ErrorResponse
ts = datetime.datetime.utcnow()
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

RegisterBlueprint = Blueprint("Register", __name__)

def validate_empty(value, field_name):
    if not value:
        return f"{field_name} cannot be empty"
    return None

def validate_create_transaksi_cuti(json_data):
    validation_errors = []

    nama = json_data.get('nama')
    alamat = json_data.get('alamat')
    status_menikah = json_data.get('status_menikah')
    usia = json_data.get('usia')
    telepon = json_data.get('telepon')
    email = json_data.get('email')
    password = json_data.get('password')

    validation_errors.extend([
        validate_empty(nama, "nama"),
        validate_empty(alamat, "alamat"),
        validate_empty(status_menikah, "status_menikah"),
        validate_empty(usia, "usia"),
        validate_empty(telepon, "telepon"),
        validate_empty(email, "email"),
        validate_empty(password, "password")
    ])

    validation_errors = [error for error in validation_errors if error is not None]

    return validation_errors

@RegisterBlueprint.route("/employee", methods=["POST"])
def create_users():
    json_data = request.json
    validation_errors = []

    nama = json_data.get('nama')
    alamat = json_data.get('alamat')
    status_menikah = json_data.get('status_menikah')
    usia = json_data.get('usia')
    telepon = json_data.get('telepon')
    email = json_data.get('email')
    password = json_data.get('password')

    existing_record_email = Employee.query.filter_by(email=email).first()

    if existing_record_email:
        return ErrorResponse("Email already exists", 400).serialize()

    try:
        json_data = json_data
        validation_errors = validate_create_transaksi_cuti(json_data)
        if validation_errors:
            return ErrorResponse(", ".join(validation_errors), 400).serialize()

        employee = Employee(
            nama=nama,
            alamat=alamat,
            telepon=telepon,
            email=email,
            foto = None,
            status_menikah=status_menikah,
            usia=usia,
            password=password,
            updated_id=None,
            deleted_id=None,
            create_at= datetime.datetime.utcnow(),
            update_at= None,
            deleted_at= None

        )
        db.session.add(employee)
        db.session.commit()
        return (
            jsonify(
                BaseResponse(
                    "{}".format(Employee.id),
                    "Register successfully",
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
    