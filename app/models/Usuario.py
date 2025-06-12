from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db
from config import Config

class User(db.Model):
    __tablename__ = 'Usuario'

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(70), nullable=True)
    apellidos = db.Column(db.String(70), nullable=True)
    correoElectronico = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column('contraseña', db.String(150), nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    direccion = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(13), nullable=True)
    departamento = db.Column(db.String(12), nullable=True)
    fotoPerfil = db.Column(db.String(200), nullable=True)

    # Relación con Carrito (un usuario puede tener un carrito)
    carrito = db.relationship('Carrito', backref='usuario', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apellidos}>'

    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'idUsuario': self.idUsuario,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'correoElectronico': self.correoElectronico,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'pais': self.pais,
            'departamento': self.departamento,
            'fotoPerfil': self.fotoPerfil
        }