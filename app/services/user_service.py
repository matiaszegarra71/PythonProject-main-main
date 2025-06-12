from app.models.user import User
from app.services.base_service import BaseService
from app import db

class UserService(BaseService):
    """Servicio para operaciones específicas de User"""

    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_all():
        """Obtener todos los usuarios"""
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        """Obtener usuario por ID"""
        return User.query.get(user_id)

    @staticmethod
    def delete(user_id):
        """Eliminar usuario"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def create(data):
        """Crear nuevo usuario con validaciones"""
        # Validar campos requeridos
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'El campo {field} es requerido')

        username = data.get('username').strip()
        email = data.get('email').strip().lower()
        password = data.get('password')
        role = data.get('role', 'client')

        # Campos opcionales de información personal
        name = data.get('name', '').strip() if data.get('name') else None
        last_name = data.get('last_name', '').strip() if data.get('last_name') else None
        phone = data.get('phone', '').strip() if data.get('phone') else None
        address = data.get('address', '').strip() if data.get('address') else None
        gender = data.get('gender')

        # Validaciones
        if len(username) < 3:
            raise ValueError('El username debe tener al menos 3 caracteres')

        if len(password) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')

        if '@' not in email:
            raise ValueError('Email inválido')

        # Validar género si se proporciona
        if gender and gender not in ['male', 'female', 'other', 'prefer_not_to_say']:
            raise ValueError('Género inválido. Opciones válidas: male, female, other, prefer_not_to_say')

        # Validar teléfono si se proporciona
        if phone and len(phone) < 7:
            raise ValueError('El teléfono debe tener al menos 7 caracteres')

        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            if existing_user.username == username:
                raise ValueError('El nombre de usuario ya está en uso')
            else:
                raise ValueError('El email ya está registrado')

        # Crear usuario
        user = User(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            gender=gender,
            role=role,
            is_active=data.get('is_active', True)
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def update(user_id, data):
        """Actualizar usuario"""
        user = User.query.get(user_id)
        if not user:
            return None

        # Campos que se pueden actualizar
        updatable_fields = ['username', 'email', 'name', 'last_name', 'phone', 'address', 'gender', 'role', 'is_active']

        for field in updatable_fields:
            if field in data:
                if field == 'username':
                    new_username = data[field].strip()
                    if len(new_username) < 3:
                        raise ValueError('El username debe tener al menos 3 caracteres')

                    # Verificar que no exista otro usuario con ese username
                    existing = User.query.filter(
                        User.username == new_username,
                        User.id != user_id
                    ).first()
                    if existing:
                        raise ValueError('El nombre de usuario ya está en uso')

                    user.username = new_username

                elif field == 'email':
                    new_email = data[field].strip().lower()
                    if '@' not in new_email:
                        raise ValueError('Email inválido')

                    # Verificar que no exista otro usuario con ese email
                    existing = User.query.filter(
                        User.email == new_email,
                        User.id != user_id
                    ).first()
                    if existing:
                        raise ValueError('El email ya está registrado')

                    user.email = new_email

                elif field == 'name':
                    user.name = data[field].strip() if data[field] else None

                elif field == 'last_name':
                    user.last_name = data[field].strip() if data[field] else None

                elif field == 'phone':
                    phone = data[field].strip() if data[field] else None
                    if phone and len(phone) < 7:
                        raise ValueError('El teléfono debe tener al menos 7 caracteres')
                    user.phone = phone

                elif field == 'address':
                    user.address = data[field].strip() if data[field] else None

                elif field == 'gender':
                    gender = data[field]
                    if gender and gender not in ['male', 'female', 'other', 'prefer_not_to_say']:
                        raise ValueError('Género inválido. Opciones válidas: male, female, other, prefer_not_to_say')
                    user.gender = gender

                elif field == 'role':
                    valid_roles = ['admin', 'manager', 'client']
                    if data[field] not in valid_roles:
                        raise ValueError(f'Rol inválido. Roles válidos: {", ".join(valid_roles)}')
                    user.role = data[field]

                elif field == 'is_active':
                    user.is_active = bool(data[field])

        # Manejar cambio de contraseña por separado
        if 'password' in data:
            new_password = data['password']
            if len(new_password) < 6:
                raise ValueError('La contraseña debe tener al menos 6 caracteres')
            user.set_password(new_password)

        db.session.commit()
        return user

    @staticmethod
    def get_user_with_notes(user_id):
        """Obtener usuario con sus notas"""
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_username(username):
        """Obtener usuario por username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        """Obtener usuario por email"""
        return User.query.filter_by(email=email.lower()).first()

    @staticmethod
    def get_active_users():
        """Obtener solo usuarios activos"""
        return User.query.filter_by(is_active=True).all()

    @staticmethod
    def get_by_role(role):
        """Obtener usuarios por rol"""
        return User.query.filter_by(role=role).all()

    @staticmethod
    def deactivate_user(user_id):
        """Desactivar usuario en lugar de eliminarlo"""
        user = User.query.get(user_id)
        if not user:
            return False

        user.is_active = False
        db.session.commit()
        return True

    @staticmethod
    def activate_user(user_id):
        """Activar usuario"""
        user = User.query.get(user_id)
        if not user:
            return False

        user.is_active = True
        db.session.commit()
        return True

    def validate_user_data(self, data, is_update=False):
        """Validar datos del usuario"""
        errors = []

        if not is_update or 'username' in data:
            if not data.get('username') or len(data['username'].strip()) < 3:
                errors.append("Username debe tener al menos 3 caracteres")

        if not is_update or 'email' in data:
            email = data.get('email', '').strip()
            if not email or '@' not in email:
                errors.append("Email debe ser válido")

        return errors
