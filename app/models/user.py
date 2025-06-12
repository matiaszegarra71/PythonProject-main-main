from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db
from config import Config

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Información personal
    name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'other', 'prefer_not_to_say', name='user_gender'), nullable=True)

    # Sistema
    role = db.Column(db.Enum('admin', 'manager', 'client', name='user_roles'),
                     nullable=False, default='client')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relación con Notes (un usuario puede tener muchas notas)
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        full_name = f"{self.name} {self.last_name}".strip() if self.name or self.last_name else self.username
        return f'<User {full_name} ({self.role})>'

    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expires_in=3600):
        """Generar token JWT"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'role': self.role,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if user and user.is_active:
                return user
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
        return None

    def has_role(self, role):
        """Verificar si el usuario tiene un rol específico"""
        return self.role == role

    def has_permission(self, required_role):
        """Verificar permisos basados en jerarquía de roles"""
        role_hierarchy = {
            'admin': 3,
            'manager': 2,
            'client': 1
        }
        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level

    def update_last_login(self):
        """Actualizar timestamp del último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    @property
    def full_name(self):
        """Obtener nombre completo"""
        if self.name and self.last_name:
            return f"{self.name} {self.last_name}"
        elif self.name:
            return self.name
        elif self.last_name:
            return self.last_name
        else:
            return self.username

    def to_dict(self, include_sensitive=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'gender': self.gender,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'notes_count': len(self.notes)
        }

        if include_sensitive:
            data['password_hash'] = self.password_hash

        return data

    def to_public_dict(self):
        """Convertir a diccionario público (sin información sensible)"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes_count': len(self.notes)
        }
