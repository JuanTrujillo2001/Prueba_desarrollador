from . import db
from flask_login import UserMixin


class Locaciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacion = db.Column(db.String(50), unique=True)
    estado = db.Column(db.Boolean(), default=True)
    users = db.relationship('User')

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50), unique=True)
    estado = db.Column(db.Boolean(), default=True)
    users = db.relationship('User')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    identificacion = db.Column(db.Integer, unique=True)
    contrasena = db.Column(db.String(150))
    localizacionID =db.Column(db.Integer, db.ForeignKey(Locaciones.id), nullable=True)
    cargoID =db.Column(db.Integer, db.ForeignKey(Cargo.id), nullable=True)
    estado = db.Column(db.Boolean(), default=True)