# TennisManager - Guía Rápida para Estudiantes

Sistema de gestión de canchas de tenis con API REST, autenticación JWT y roles de usuario.

## 🚀 Inicio Rápido

### 1. Requisitos
- Docker
- Docker Compose

### 2. Levantar el Proyecto
```bash
# Clonar el repositorio
git clone <tu-repo-url>
cd PythonProyect

# Levantar servicios
make up-build

# Ver logs (opcional)
make logs
```

### 3. Acceder a la Aplicación
- **Web**: http://localhost:5001/
- **API Health**: http://localhost:5001/health

## 🔐 Usuarios de Prueba

| Usuario | Contraseña | Rol | Email |
|---------|------------|-----|-------|
| admin | admin123 | admin | admin@tennismanager.com |
| manager1 | manager123 | manager | manager@tennismanager.com |
| eidan | eidan123 | client | eidan@tennismanager.com |

## 📚 API Principales

### Autenticación
```bash
# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "eidan", "password": "eidan123"}'

# Registro
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "nuevo@example.com",
    "password": "password123",
    "name": "Nombre",
    "last_name": "Apellido"
  }'
```

### Usuarios (requiere token)
```bash
# Obtener token primero
TOKEN="tu_jwt_token_aqui"

# Listar usuarios (admin/manager)
curl -X GET http://localhost:5001/api/users \
  -H "Authorization: Bearer $TOKEN"

# Ver perfil
curl -X GET http://localhost:5001/api/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Notas (requiere token)
```bash
# Listar notas
curl -X GET http://localhost:5001/api/notes \
  -H "Authorization: Bearer $TOKEN"

# Crear nota
curl -X POST http://localhost:5001/api/notes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Nota",
    "content": "Contenido de la nota"
  }'
```

## 🛠️ Comandos Útiles

```bash
# Reiniciar base de datos
make reset-db

# Ver logs
make logs

# Parar servicios
make down

# Reconstruir todo
make rebuild

# Probar login
make test-login

# Entrar al contenedor para debugging
make debug
```

## 🏗️ Estructura del Proyecto

```
├── app/
│   ├── models/          # Modelos (User, Note)
│   ├── controllers/     # Controladores (API endpoints)
│   ├── services/        # Lógica de negocio
│   └── utils/           # Decoradores de autenticación
├── config.py           # Configuración
├── reset_db.py         # Script para reiniciar DB
├── Makefile           # Comandos útiles
└── docker-compose.yml # Configuración Docker
```

## 🔑 Sistema de Roles

- **admin**: Acceso total al sistema
- **manager**: Gestión de usuarios y notas
- **client**: Solo sus propias notas

## 🐛 Problemas Comunes

### Puerto ocupado
Si el puerto 5001 está ocupado, cambiar en `docker-compose.yml`:
```yaml
ports:
  - "5002:5000"  # Cambiar 5001 por 5002
```

### Base de datos no conecta
```bash
# Ver logs de la base de datos
make logs-db

# Reiniciar servicios
make down && make up-build
```

### Permisos en Docker
```bash
# En Linux/Mac, dar permisos
sudo chmod +x reset_db.py
```

## 📱 Probar con Postman

1. Importar colección: `TennisManager_API_Collection.postman_collection.json`
2. Hacer login para obtener token
3. El token se guarda automáticamente
4. Probar otros endpoints

## 🎯 Ejercicios Sugeridos

1. **Básico**: Hacer login y ver tu perfil
2. **Intermedio**: Crear y listar notas
3. **Avanzado**: Crear un nuevo usuario como admin
4. **Desafío**: Implementar un nuevo endpoint

---

**¿Problemas?** Revisar logs con `make logs` o preguntar al profesor.

**Versión**: 3.0 con JWT Auth
**Stack**: Flask 3.0 + MySQL 8.0 + Docker
