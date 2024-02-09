import os
from app import db

from models.employee import Employee
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
from common.InvalidUUID import InvalidUUIDError


class EmployeeRepository(db.Model):
    __tablename__ = "employee"

    def get_by_id_user(id):
        try:
            id_user_uuid = uuid.UUID(id)
        except ValueError:
            raise InvalidUUIDError("Id is required!")
        data = Employee.query.filter(
            Employee.user_id==id
        ).first()
        return data


    def get_by_nip(nip):
        data = Employee.query.filter_by(nip=nip).first()
        return data

    def get_by_phone(nip):
        data = Employee.query.filter_by(nip=nip).first()
        return data
    
    def get_by_email(email):
        data = Employee.query.filter_by(email=email).first()
        return data

    def get_list(filter, page, limit):
        try:
            search = f"%{filter}%" if filter else None
            data_query = (
                Employee.query
                .filter(
                    Employee.deleted_id.is_(None),
                    (Employee.nama.ilike(search) if search else True) 
                )
                .order_by(Employee.nama)  # Adjust the ordering as needed
                .paginate(page=page, per_page=limit, error_out=False)
            )
            return data_query.items
        except Exception as e:
            print(str(e))
            raise Exception(str(e))
        
    def get_count_all_employee():
        data = Employee.query.filter(Employee.deleted_at == None).all()
        return data

    def get_count(search):
        try:
            data = Employee.query.filter(Employee.deleted_at == None)
            if search != "":
                search = "%{}%".format(search)
                data = data.filter(Employee.nama.ilike(search))
            data = data.all()
            return data
        except Exception as e:
            print(str(e))
            raise Exception(str(e))
        
  