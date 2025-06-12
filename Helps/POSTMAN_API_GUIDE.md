# 🎾 TennisManager API v3.0 - Guía de Postman

## 📋 Descripción
Esta es la colección completa de Postman para la API REST de TennisManager con autenticación JWT y sistema de roles.

## 🚀 Configuración Inicial

### 1. Importar la Colección
1. Abre Postman
2. Haz clic en "Import"
3. Selecciona el archivo `TennisManager_API_Collection.postman_collection.json`
4. La colección se importará con todas las variables configuradas

### 2. Variables de Entorno
La colección incluye estas variables automáticamente:
- `base_url`: http://localhost:5001
- `jwt_token`: Se actualiza automáticamente al hacer login

### 3. Asegurar que la Aplicación esté Corriendo
```bash
# En tu terminal, desde el directorio del proyecto:
make up
make reset-db  # Para tener datos de prueba
```

## 👥 Usuarios de Prueba Disponibles

| Username | Email | Password | Rol | Descripción |
|----------|-------|----------|-----|-------------|
| `admin` | `admin@tennismanager.com` | `admin123` | admin | Acceso completo a todo |
| `manager1` | `manager1@tennismanager.com` | `manager123` | manager | Gestión de usuarios y notas |
| `eidan` | `eidan@tennismanager.com` | `eidan123` | client | Usuario cliente básico |
| `maria_coach` | `maria@tennismanager.com` | `maria123` | client | Usuario cliente básico |
| `carlos_player` | `carlos@tennismanager.com` | `carlos123` | client | Usuario cliente básico |

## 🔐 Flujo de Autenticación

### Paso 1: Login
1. Ve a la carpeta "🔐 Autenticación"
2. Ejecuta cualquiera de los requests de login:
   - "Login - Admin (por username)" - Usa el username
   - "Login - Admin (por email)" - Usa el email
   - "Login - Manager" - Para gestión
   - "Login - Client (Eidan)" - Para acceso básico

**El token JWT se guardará automáticamente** en la variable `jwt_token` gracias al script de test incluido.

### Paso 2: Usar Endpoints Protegidos
Una vez logueado, todos los demás endpoints usarán automáticamente el token guardado.

### 🔑 Métodos de Login
La API acepta login de dos formas:
1. **Por Username**: `{"username": "admin", "password": "admin123"}`
2. **Por Email**: `{"username": "admin@tennismanager.com", "password": "admin123"}`

*Nota: El campo se llama "username" pero acepta tanto username como email*

## 📚 Estructura de la API

### 🏠 Endpoints Públicos (Sin autenticación)
- `GET /` - Landing page
- `GET /health` - Health check
- `GET /api-info` - Información de la API

### 🔐 Autenticación
- `POST /api/auth/login` - Iniciar sesión (username o email)
- `POST /api/auth/register` - Registrar nuevo usuario
- `GET /api/auth/validate` - Validar token JWT
- `GET /api/auth/profile` - Obtener perfil del usuario
- `PUT /api/auth/change-password` - Cambiar contraseña
- `GET /api/auth/users` - Listar usuarios (solo admin)

### 👥 Gestión de Usuarios
- `GET /api/users` - Listar usuarios (requiere manager+)
- `GET /api/users/{id}` - Obtener usuario específico
- `GET /api/users/{id}/notes` - Obtener usuario con sus notas
- `POST /api/users` - Crear usuario (solo admin)
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario (solo admin)

### 📝 Gestión de Notas
- `GET /api/notes` - Listar notas (filtradas por permisos)
- `GET /api/notes/{id}` - Obtener nota específica
- `GET /api/notes/search` - Buscar notas por título
- `POST /api/notes` - Crear nota
- `PUT /api/notes/{id}` - Actualizar nota
- `DELETE /api/notes/{id}` - Eliminar nota

## 🛡️ Sistema de Permisos

### Roles y Jerarquía
1. **admin** (nivel 3): Acceso completo
2. **manager** (nivel 2): Gestión de usuarios y notas
3. **client** (nivel 1): Acceso básico a sus propios recursos

### Reglas de Acceso

#### Usuarios
- **Ver lista**: manager+
- **Ver perfil**: propio perfil o manager+
- **Crear**: solo admin
- **Actualizar**: propio perfil o admin
- **Eliminar**: solo admin

#### Notas
- **Ver**: propias notas o manager+ (ve todas)
- **Crear**: cualquier usuario autenticado
- **Actualizar**: propias notas o manager+
- **Eliminar**: propias notas o manager+

## 🧪 Casos de Prueba Incluidos

La carpeta "🧪 Casos de Prueba" incluye ejemplos de errores comunes:
- Login con credenciales incorrectas
- Acceso sin token
- Acceso con token inválido
- Cliente intentando acceder a endpoints de manager
- Registro con datos inválidos

## 📝 Ejemplos de Uso

### 1. Flujo Completo de Admin
```
1. Login - Admin (por username o email)
2. Listar Todos los Usuarios (Solo Admin)
3. Crear Usuario (Solo Admin)
4. Listar Todas las Notas
5. Crear Nota
```

### 2. Flujo de Manager
```
1. Login - Manager
2. Listar Usuarios (Manager+)
3. Obtener Usuario con Notas
4. Crear Nota
5. Actualizar Nota
```

### 3. Flujo de Cliente
```
1. Login - Client (Eidan)
2. Obtener Perfil
3. Crear Nota (Sin especificar user_id)
4. Listar Todas las Notas (solo verá las suyas)
5. Actualizar Nota (solo las suyas)
```

## 🔄 Respuestas de la API

### Formato Estándar de Respuesta
```json
{
    "success": true,
    "message": "Mensaje descriptivo",
    "data": {
        // Datos de respuesta
    },
    "timestamp": "2025-01-XX 10:XX:XX"
}
```

### Respuesta de Login Exitoso
```json
{
    "success": true,
    "message": "Login exitoso",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@tennismanager.com",
            "role": "admin",
            "is_active": true
        }
    },
    "timestamp": "2025-01-XX 10:XX:XX"
}
```

### Respuesta de Error
```json
{
    "success": false,
    "message": "Credenciales inválidas",
    "error": "INVALID_CREDENTIALS",
    "timestamp": "2025-01-XX 10:XX:XX"
}
```

## 🚨 Códigos de Error Comunes

| Código | Descripción |
|--------|-------------|
| 401 | No autorizado (sin token o token inválido) |
| 403 | Prohibido (sin permisos suficientes) |
| 404 | Recurso no encontrado |
| 400 | Datos de entrada inválidos |
| 409 | Conflicto (ej: username ya existe) |
| 500 | Error interno del servidor |

## 🔒 Seguridad y Buenas Prácticas

### Passwords en Postman
- Los passwords en los ejemplos son solo para desarrollo/testing
- En producción, usa passwords seguros con:
  - Mínimo 8 caracteres
  - Mayúsculas y minúsculas
  - Números y símbolos especiales
  - Ejemplo: `SecurePass123!`

### Manejo de Tokens
- Los tokens JWT expiran en 1 hora
- Se guardan automáticamente en la variable `jwt_token`
- Si expira, simplemente vuelve a hacer login

### Login Flexible
- Puedes usar username O email en el campo "username"
- Ejemplos:
  ```json
  {"username": "admin", "password": "admin123"}
  {"username": "admin@tennismanager.com", "password": "admin123"}
  ```

## 💡 Tips de Uso

1. **Siempre hacer login primero** - El token se guarda automáticamente
2. **Revisar los permisos** - Algunos endpoints requieren roles específicos
3. **Usar los casos de prueba** - Para entender los errores comunes
4. **Verificar la aplicación** - Asegúrate de que esté corriendo en localhost:5001
5. **Revisar logs** - Si hay errores, revisa los logs de Docker
6. **Login flexible** - Puedes usar username o email indistintamente

## 🔧 Troubleshooting

### Error de Conexión
```bash
# Verificar que la aplicación esté corriendo
make status
make logs

# Si no está corriendo
make up
```

### Token Expirado
- Simplemente vuelve a hacer login
- Los tokens expiran en 1 hora

### Permisos Insuficientes
- Verifica que estés usando el usuario correcto para el endpoint
- Revisa la tabla de permisos arriba

### Datos No Encontrados
```bash
# Reiniciar la base de datos con datos de prueba
make reset-db
```

### Login Fallido
- Verifica username/email y password
- Puedes usar cualquiera de los dos formatos:
  - `"username": "admin"`
  - `"username": "admin@tennismanager.com"`

## 📞 Soporte

Si encuentras algún problema:
1. Revisa los logs: `make logs`
2. Verifica el estado: `make status`
3. Reinicia si es necesario: `make restart`
4. Resetea la DB si faltan datos: `make reset-db`

¡Disfruta probando la API de TennisManager! 🎾
