.PHONY: help up up-build up-logs down logs logs-app logs-db health init-db reset-db rebuild clean dev-install dev-run test-health test-users test-notes test-auth test-login debug shell debug-example attach debug-logs python ipython flask-shell

# Variables
COMPOSE_FILE = docker-compose.yml
APP_SERVICE = web
DB_SERVICE = db

help: ## Mostrar ayuda
	@echo "🎾 TennisManager SaaS - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 🚀 Comandos principales
up: ## Ejecutar aplicación en segundo plano
	docker compose -f $(COMPOSE_FILE) up -d

up-build: ## Construir y ejecutar aplicación
	docker compose -f $(COMPOSE_FILE) up -d --build

up-logs: ## Ejecutar aplicación con logs visibles
	docker compose -f $(COMPOSE_FILE) up --build

down: ## Detener aplicación
	docker compose -f $(COMPOSE_FILE) down

logs: ## Ver logs de todos los servicios
	docker compose -f $(COMPOSE_FILE) logs -f

logs-app: ## Ver logs solo de la aplicación
	docker compose -f $(COMPOSE_FILE) logs -f $(APP_SERVICE)

logs-db: ## Ver logs solo de la base de datos
	docker compose -f $(COMPOSE_FILE) logs -f $(DB_SERVICE)

health: ## Verificar estado de la aplicación
	@echo "🏥 Verificando estado de TennisManager..."
	@curl -s http://localhost:5001/health | jq '.' || echo "❌ Aplicación no disponible"

# 🐛 Comandos de debugging
debug: ## Entrar al contenedor web para debugging interactivo
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) /bin/bash

shell: ## Alias para debug - shell interactivo
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) /bin/bash

debug-example: ## Ejecutar ejemplo de debugging
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python debug_example.py

attach: ## Información sobre cómo attachear a un contenedor
	@echo "🐛 Para attachear a un contenedor con debugging:"
	@echo "1. Pon un breakpoint en tu código: import ipdb; ipdb.set_trace()"
	@echo "2. Ejecuta: make attach-web"
	@echo "3. Interactúa con el debugger"

attach-web: ## Attachear al contenedor web
	docker attach $$(docker compose -f $(COMPOSE_FILE) ps -q $(APP_SERVICE))

debug-logs: ## Ver logs en tiempo real para debugging
	docker compose -f $(COMPOSE_FILE) logs -f --tail=100

# 🐍 Comandos de Python
python: ## Ejecutar Python en el contenedor
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python

ipython: ## Ejecutar IPython en el contenedor
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) ipython

flask-shell: ## Ejecutar Flask shell
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) flask shell

# 🗄️ Comandos de base de datos
init-db: ## Inicializar base de datos con datos de ejemplo (DEPRECATED - usar reset-db)
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python init_db.py

reset-db: ## Borrar y recrear tablas con datos de autenticación
	@echo "🔄 Reiniciando base de datos con autenticación JWT..."
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) python reset_db.py

rebuild: ## Reconstruir completamente la aplicación
	docker compose -f $(COMPOSE_FILE) down -v
	docker compose -f $(COMPOSE_FILE) build --no-cache
	docker compose -f $(COMPOSE_FILE) up -d

clean: ## Limpiar contenedores y volúmenes
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f

# Desarrollo local
dev-install: ## Instalar dependencias para desarrollo local
	pip install -r requirements.txt

dev-run: ## Ejecutar aplicación en modo desarrollo local
	export FLASK_APP=app.py && export FLASK_ENV=development && python app.py

# Tests de API
test-health: ## Probar endpoint de health check
	@echo "🏥 Probando health check..."
	@curl -s http://localhost:5001/health | jq '.'

test-users: ## Probar endpoint de usuarios (requiere autenticación)
	@echo "👥 Probando endpoint de usuarios..."
	@echo "⚠️  Este endpoint requiere autenticación. Usa test-login primero."
	@curl -s http://localhost:5001/api/users | jq '.'

test-notes: ## Probar endpoint de notas (requiere autenticación)
	@echo "📝 Probando endpoint de notas..."
	@echo "⚠️  Este endpoint requiere autenticación. Usa test-login primero."
	@curl -s http://localhost:5001/api/notes | jq '.'

# Tests de autenticación
test-auth: ## Probar todos los endpoints de autenticación
	@echo "🔐 Probando sistema de autenticación completo..."
	@make test-login
	@echo ""
	@make test-register
	@echo ""
	@make test-validate

test-login: ## Probar login con usuario de ejemplo
	@echo "🔐 Probando login con usuario 'eidan'..."
	@curl -s -X POST http://localhost:5001/api/auth/login \
		-H "Content-Type: application/json" \
		-d '{"username": "eidan", "password": "eidan123"}' | jq '.'

test-register: ## Probar registro de nuevo usuario
	@echo "📝 Probando registro de nuevo usuario..."
	@curl -s -X POST http://localhost:5001/api/auth/register \
		-H "Content-Type: application/json" \
		-d '{"username": "test_user", "email": "test@example.com", "password": "test123"}' | jq '.'

test-validate: ## Probar validación de token (requiere token válido)
	@echo "✅ Para probar validación, primero haz login y usa el token:"
	@echo "curl -H 'Authorization: Bearer YOUR_TOKEN' http://localhost:5001/api/auth/validate"

test-admin: ## Probar login con usuario admin
	@echo "👑 Probando login con usuario admin..."
	@curl -s -X POST http://localhost:5001/api/auth/login \
		-H "Content-Type: application/json" \
		-d '{"username": "admin", "password": "admin123"}' | jq '.'

test-manager: ## Probar login con usuario manager
	@echo "👔 Probando login con usuario manager..."
	@curl -s -X POST http://localhost:5001/api/auth/login \
		-H "Content-Type: application/json" \
		-d '{"username": "manager1", "password": "manager123"}' | jq '.'

# Información útil
info: ## Mostrar información de la aplicación
	@echo "🎾 TennisManager SaaS v3.0 - Con autenticación JWT"
	@echo ""
	@echo "🌐 URLs principales:"
	@echo "   Landing Page:  http://localhost:5001/"
	@echo "   Health Check:  http://localhost:5001/health"
	@echo "   API Info:      http://localhost:5001/api-info"
	@echo ""
	@echo "🔐 Endpoints de autenticación:"
	@echo "   Login:         POST http://localhost:5001/api/auth/login"
	@echo "   Registro:      POST http://localhost:5001/api/auth/register"
	@echo "   Validar:       GET  http://localhost:5001/api/auth/validate"
	@echo "   Perfil:        GET  http://localhost:5001/api/auth/profile"
	@echo ""
	@echo "🔑 Usuarios de prueba:"
	@echo "   admin (admin123) - Rol: admin"
	@echo "   manager1 (manager123) - Rol: manager"
	@echo "   eidan (eidan123) - Rol: client"
	@echo ""
	@echo "📚 Comandos útiles:"
	@echo "   make reset-db  - Reiniciar base de datos"
	@echo "   make test-auth - Probar autenticación"
	@echo "   make logs      - Ver logs en tiempo real"
	@echo "   make debug     - Entrar al contenedor para debugging"
