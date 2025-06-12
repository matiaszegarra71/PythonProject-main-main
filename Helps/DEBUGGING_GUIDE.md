# 🐛 Guía de Debugging en Python con Docker
## Equivalente a `byebug` en Ruby on Rails

Esta guía te muestra cómo debuggear tu aplicación Flask TennisManager usando Python con Docker, similar a como usarías `byebug` en Ruby on Rails.

## 🚀 Configuración Inicial

### 1. Dependencias Instaladas
Ya tienes `ipdb` instalado en `requirements.txt`:
```
ipdb==0.13.13
```

### 2. Docker Configurado
El `docker-compose.yml` está configurado con:
```yaml
stdin_open: true  # Permite input interactivo
tty: true        # Permite terminal interactivo
```

## 🐍 Métodos de Debugging

### 1. **`ipdb.set_trace()` - RECOMENDADO**
```python
import ipdb
ipdb.set_trace()  # ⬅️ Equivalente a byebug
```

### 2. **`breakpoint()` - Python 3.7+**
```python
breakpoint()  # ⬅️ Forma moderna
```

### 3. **`pdb.set_trace()` - Nativo**
```python
import pdb
pdb.set_trace()  # ⬅️ Básico pero funcional
```

## 🐳 Cómo Debuggear con Docker

### Método 1: Debugging Interactivo (RECOMENDADO)

1. **Agregar breakpoint en tu código:**
```python
# En app/controllers/auth_controller.py
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    import ipdb; ipdb.set_trace()  # ⬅️ BREAKPOINT AQUÍ

    # Tu código continúa...
```

2. **Ejecutar la aplicación:**
```bash
make up
```

3. **Hacer request que active el breakpoint:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

4. **Attachear al contenedor:**
```bash
make debug
# O directamente:
docker-compose exec web /bin/bash
```

5. **El debugger estará activo en la terminal del contenedor**

### Método 2: Usando Docker Attach

1. **Agregar breakpoint en tu código**
2. **Encontrar el container ID:**
```bash
docker-compose ps
```

3. **Attachear directamente:**
```bash
docker attach <container_id>
```

### Método 3: Debugging con Logs

1. **Ver logs en tiempo real:**
```bash
make debug-logs
# O:
docker-compose logs -f web
```

## 🎯 Ejemplos Prácticos

### Debugging en AuthController

```python
# app/controllers/auth_controller.py
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # 🐛 BREAKPOINT: Ver datos recibidos
        import ipdb; ipdb.set_trace()

        username = data.get('username')
        password = data.get('password')

        # Buscar usuario
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        # 🐛 BREAKPOINT: Ver si se encontró el usuario
        import ipdb; ipdb.set_trace()

        if not user:
            return error_response('Credenciales inválidas', 401)

        # Verificar contraseña
        if not user.check_password(password):
            return error_response('Credenciales inválidas', 401)

        # 🐛 BREAKPOINT: Ver token generado
        token = user.generate_token()
        import ipdb; ipdb.set_trace()

        return success_response('Login exitoso', {'token': token})

    except Exception as e:
        # 🐛 BREAKPOINT: Debugging en excepciones
        import ipdb; ipdb.set_trace()
        return error_response(f'Error: {str(e)}', 500)
```

### Debugging Condicional

```python
# Solo debuggear para usuarios específicos
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')

    # Solo debuggear para el usuario 'eidan'
    if username == 'eidan':
        import ipdb; ipdb.set_trace()

    # Tu lógica continúa...
```

### Debugging con Headers

```python
# Solo debuggear si hay un header específico
@auth_bp.route('/api/auth/validate', methods=['GET'])
def validate():
    debug_mode = request.headers.get('X-Debug-Mode') == 'true'

    if debug_mode:
        import ipdb; ipdb.set_trace()

    # Tu lógica continúa...
```

## 🛠️ Comandos del Debugger

Una vez en el debugger (similar a byebug):

| Comando | Descripción |
|---------|-------------|
| `n` | Next line (siguiente línea) |
| `s` | Step into (entrar en función) |
| `c` | Continue (continuar ejecución) |
| `l` | List (mostrar código actual) |
| `p variable` | Print variable |
| `pp variable` | Pretty print variable |
| `h` | Help (ayuda) |
| `q` | Quit (salir) |
| `u` | Up (subir en stack) |
| `d` | Down (bajar en stack) |
| `w` | Where (mostrar stack trace) |

### Ejemplos de Uso en el Debugger:

```python
# En el debugger:
(Pdb) p data
{'username': 'admin', 'password': 'admin123'}

(Pdb) p user
<User admin@tennismanager.com>

(Pdb) p user.role
<UserRole.admin: 'admin'>

(Pdb) pp user.__dict__
{'id': 1,
 'username': 'admin',
 'email': 'admin@tennismanager.com',
 'role': <UserRole.admin: 'admin'>}

(Pdb) n  # Siguiente línea
(Pdb) c  # Continuar
```

## 🚀 Comandos Make para Debugging

```bash
# Entrar al contenedor para debugging
make debug

# Ver logs en tiempo real
make debug-logs

# Ejecutar ejemplo de debugging
make debug-example

# Attachear a contenedor (similar a docker attach)
make attach-web

# Shell interactivo
make shell

# Python interactivo
make python

# IPython interactivo
make ipython
```

## 🎯 Flujo de Trabajo Recomendado

### 1. Debugging Rápido
```bash
# 1. Agregar breakpoint en código
import ipdb; ipdb.set_trace()

# 2. Levantar aplicación
make up

# 3. Hacer request
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 4. Entrar al contenedor
make debug

# 5. Debuggear en la terminal
```

### 2. Debugging Avanzado
```bash
# 1. Ver logs en tiempo real
make debug-logs

# 2. En otra terminal, entrar al contenedor
make debug

# 3. Hacer requests y debuggear
```

## 🔍 Debugging Post-Mortem

Para debuggear después de una excepción:

```python
try:
    # Código que puede fallar
    resultado = 10 / 0
except Exception as e:
    import ipdb
    ipdb.post_mortem()  # ⬅️ Debugging después del error
```

## 🧪 Ejemplos de Testing con Debugging

### Test de Login con Debugging
```bash
# 1. Agregar breakpoint en login
# 2. Ejecutar test
make test-login

# 3. El debugger se activará automáticamente
```

### Test Específico
```python
# En tu código de test
def test_login_debug():
    import ipdb; ipdb.set_trace()

    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })

    # Debuggear respuesta
    import ipdb; ipdb.set_trace()
    assert response.status_code == 200
```

## 💡 Tips y Trucos

### 1. Debugging Temporal
```python
# Usar solo durante desarrollo
if app.debug:
    import ipdb; ipdb.set_trace()
```

### 2. Debugging con Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def login():
    logger.debug("Iniciando login")
    import ipdb; ipdb.set_trace()
    # Tu código...
```

### 3. Debugging Remoto (Avanzado)
```python
# Para debugging remoto
import ipdb
ipdb.set_trace(context=21)  # Más líneas de contexto
```

## 🚨 Troubleshooting

### Problema: El debugger no se activa
**Solución:**
```bash
# Verificar que el contenedor tenga stdin_open y tty
docker-compose exec web /bin/bash
# Si no funciona, revisar docker-compose.yml
```

### Problema: No puedo ver el debugger
**Solución:**
```bash
# Attachear directamente al contenedor
docker attach $(docker-compose ps -q web)
```

### Problema: El debugger se cuelga
**Solución:**
```bash
# Reiniciar contenedor
make restart
# O forzar salida
docker-compose kill web
docker-compose up web
```

## 📚 Recursos Adicionales

- [Documentación oficial de pdb](https://docs.python.org/3/library/pdb.html)
- [IPython Debugger (ipdb)](https://github.com/gotcha/ipdb)
- [Debugging en Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)

¡Ahora puedes debuggear tu aplicación Python como un pro! 🐍🐛
