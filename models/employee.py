from datetime import datetime
from app import db, app
import uuid
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(CHAR(250), primary_key=True, default=str(uuid.uuid4()))
    nama = db.Column(db.String(250), nullable = True)
    alamat = db.Column(db.String(250), nullable = True)
    foto = db.Column(db.String(250), nullable = True)
    status_menikah = db.Column(db.String(250), nullable = True)
    usia = db.Column(db.String(50), nullable = True)
    telepon = db.Column(db.String(20), nullable = True)
    email = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(250), nullable = False)

    updated_id = db.Column(CHAR(250), nullable=True, default=str(uuid.uuid4()))
    deleted_id = db.Column(CHAR(250), nullable=True, default=str(uuid.uuid4()))
    create_at = db.Column(DateTime, nullable=True)
    update_at = db.Column(DateTime, nullable=True)
    deleted_at = db.Column(DateTime, nullable=True)    

    def __init__(
        self,
        nama,
        alamat,
        foto,
        status_menikah,
        usia,
        telepon,
        email,
        password,
        updated_id,  
        deleted_id,
        create_at,
        update_at,
        deleted_at
    ):
        self.nama = nama
        self.alamat = alamat
        self.foto = foto
        self.status_menikah = status_menikah
        self.usia = usia
        self.telepon = telepon
        self.email = email
        self.setPassword(password)
        self.updated_id = updated_id
        self.deleted_id = deleted_id
        self.create_at = create_at
        self.update_at = update_at
        self.deleted_at = deleted_at

    
    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "alamat": self.alamat,
            "foto": self.foto,
            "status_menikah": self.status_menikah,
            "usia": self.usia,
            "telepon": self.telepon,
            "email": self.email,
            "updated_id": self.updated_id,
            "deleted_id": self.deleted_id,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "deleted_at": self.deleted_at
        }
    
 