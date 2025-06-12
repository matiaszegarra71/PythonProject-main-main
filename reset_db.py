#!/usr/bin/env python3
"""
Script para borrar y recrear las tablas de la base de datos con datos de ejemplo
que incluyen autenticación JWT y roles
"""

import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.note import Note

def reset_database():
    """Borrar y recrear base de datos con datos de ejemplo"""

    # Crear aplicación
    app = create_app('development')

    with app.app_context():
        print("🗑️  Borrando tablas existentes...")
        db.drop_all()

        print("🗄️  Creando nuevas tablas...")
        db.create_all()

        print("👤 Creando usuarios con autenticación...")

        # Crear usuarios de ejemplo con diferentes roles
        users_data = [
            {
                "username": "admin",
                "email": "admin@tennismanager.com",
                "password": "admin123",
                "role": "admin",
                "name": "Administrador",
                "last_name": "Sistema",
                "phone": "+1234567890",
                "address": "Oficina Central, Tennis Club",
                "gender": "prefer_not_to_say"
            },
            {
                "username": "manager1",
                "email": "manager@tennismanager.com",
                "password": "manager123",
                "role": "manager",
                "name": "Ana",
                "last_name": "García",
                "phone": "+1234567891",
                "address": "Av. Principal 123, Ciudad",
                "gender": "female"
            },
            {
                "username": "eidan",
                "email": "eidan@tennismanager.com",
                "password": "eidan123",
                "role": "client",
                "name": "Eidan",
                "last_name": "Rosado",
                "phone": "+1234567892",
                "address": "Calle Secundaria 456, Ciudad",
                "gender": "male"
            },
            {
                "username": "maria_coach",
                "email": "maria@tennismanager.com",
                "password": "maria123",
                "role": "client",
                "name": "María",
                "last_name": "López",
                "phone": "+1234567893",
                "address": "Zona Deportiva 789, Ciudad",
                "gender": "female"
            },
            {
                "username": "carlos_player",
                "email": "carlos@tennismanager.com",
                "password": "carlos123",
                "role": "client",
                "name": "Carlos",
                "last_name": "Martínez",
                "phone": "+1234567894",
                "address": "Barrio Norte 321, Ciudad",
                "gender": "male"
            }
        ]

        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                name=user_data["name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                address=user_data["address"],
                gender=user_data["gender"],
                role=user_data["role"]
            )
            user.set_password(user_data["password"])
            db.session.add(user)
            users.append(user)

        db.session.commit()
        print(f"✅ Creados {len(users)} usuarios con autenticación")

        print("📝 Creando notas de ejemplo...")

        # Crear notas de ejemplo relacionadas con gestión de canchas de tenis
        notes_data = [
            {"title": "Reserva Cancha Central", "content": "Cancha reservada para torneo del sábado 15:00-17:00", "user_id": users[0].id},
            {"title": "Mantenimiento Cancha 3", "content": "Programar mantenimiento de superficie y red para el lunes", "user_id": users[0].id},
            {"title": "Lista de Jugadores VIP", "content": "Actualizar lista de miembros premium para acceso prioritario", "user_id": users[1].id},
            {"title": "Horarios de Entrenamiento", "content": "Lunes y Miércoles 18:00-20:00 - Clases grupales", "user_id": users[1].id},
            {"title": "Equipamiento Nuevo", "content": "Solicitar presupuesto para nuevas raquetas de alquiler", "user_id": users[2].id},
            {"title": "Evento Fin de Semana", "content": "Organizar torneo amateur para el próximo domingo", "user_id": users[2].id},
            {"title": "Membresía Anual", "content": "Renovar membresía premium - vence el 31/12", "user_id": users[3].id},
            {"title": "Clases Particulares", "content": "Agendar clase con instructor profesional", "user_id": users[4].id}
        ]

        notes = []
        for note_data in notes_data:
            note = Note(**note_data)
            db.session.add(note)
            notes.append(note)

        db.session.commit()
        print(f"✅ Creadas {len(notes)} notas")

        print("\n🎉 Base de datos reinicializada correctamente!")
        print("\n📊 Resumen:")
        print(f"   👤 Usuarios: {User.query.count()}")
        print(f"   📝 Notas: {Note.query.count()}")

        print("\n🔐 Usuarios de prueba creados:")
        for user in users:
            print(f"   👤 {user.username} ({user.role}) - Email: {user.email}")

        print("\n🔑 Contraseñas de prueba:")
        print("   🔐 admin: admin123")
        print("   🔐 manager1: manager123")
        print("   🔐 eidan: eidan123")
        print("   🔐 maria_coach: maria123")
        print("   🔐 carlos_player: carlos123")

        print("\n🌐 TennisManager SaaS - Endpoints de autenticación:")
        print("   🔐 Login:         POST http://localhost:5001/api/auth/login")
        print("   📝 Registro:      POST http://localhost:5001/api/auth/register")
        print("   ✅ Validar:       GET  http://localhost:5001/api/auth/validate")
        print("   👤 Perfil:        GET  http://localhost:5001/api/auth/profile")
        print("   🔄 Cambiar Pass:  PUT  http://localhost:5001/api/auth/change-password")

        print("\n🌐 Endpoints protegidos:")
        print("   👥 Usuarios:      GET  http://localhost:5001/api/users (requiere manager+)")
        print("   📝 Notas:         GET  http://localhost:5001/api/notes (requiere token)")
        print("   🏠 Landing Page:  GET  http://localhost:5001/")
        print("   💚 Health Check:  GET  http://localhost:5001/health")

        print("\n🎾 ¡TennisManager con autenticación JWT está listo!")
        print("\n💡 Ejemplo de login:")
        print('   curl -X POST http://localhost:5001/api/auth/login \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"username": "eidan", "password": "eidan123"}\'')

if __name__ == "__main__":
    reset_database()
