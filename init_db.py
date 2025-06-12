#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""

import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.note import Note

def init_database():
    """Inicializar base de datos con datos de ejemplo"""

    # Crear aplicación
    app = create_app('development')

    with app.app_context():
        print("🗄️  Creando tablas...")
        db.create_all()

        # Verificar si ya hay datos
        if User.query.first():
            print("⚠️  La base de datos ya contiene datos.")
            return

        print("👤 Creando usuarios de ejemplo...")

        # Crear usuarios de ejemplo para TennisManager
        users_data = [
            {"username": "eidan", "email": "eidan@tennismanager.com"},
            {"username": "maria_coach", "email": "maria@tennismanager.com"},
            {"username": "carlos_admin", "email": "carlos@tennismanager.com"},
            {"username": "ana_player", "email": "ana@tennismanager.com"},
            {"username": "luis_member", "email": "luis@tennismanager.com"}
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            users.append(user)

        db.session.commit()
        print(f"✅ Creados {len(users)} usuarios")

        print("📝 Creando notas de ejemplo...")

        # Crear notas de ejemplo relacionadas con gestión de canchas de tenis
        notes_data = [
            {"title": "Reserva Cancha Central", "content": "Cancha reservada para torneo del sábado 15:00-17:00", "user_id": users[0].id},
            {"title": "Mantenimiento Cancha 3", "content": "Programar mantenimiento de superficie y red para el lunes", "user_id": users[0].id},
            {"title": "Lista de Jugadores VIP", "content": "Actualizar lista de miembros premium para acceso prioritario", "user_id": users[0].id},
            {"title": "Horarios de Entrenamiento", "content": "Lunes y Miércoles 18:00-20:00 - Clases grupales", "user_id": users[1].id},
            {"title": "Equipamiento Nuevo", "content": "Solicitar presupuesto para nuevas raquetas de alquiler", "user_id": users[1].id},
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

        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📊 Resumen:")
        print(f"   👤 Usuarios: {User.query.count()}")
        print(f"   📝 Notas: {Note.query.count()}")

        print("\n🌐 TennisManager SaaS - Endpoints disponibles:")
        print("   🏠 Landing Page:  http://localhost:5001/")
        print("   💚 Health Check:  http://localhost:5001/health")
        print("   📊 API Info:      http://localhost:5001/api-info")
        print("   👥 Usuarios API:  http://localhost:5001/api/users")
        print("   📝 Notas API:     http://localhost:5001/api/notes")

        print("\n🎾 ¡TennisManager está listo para gestionar tu club de tenis!")

if __name__ == "__main__":
    init_database()
