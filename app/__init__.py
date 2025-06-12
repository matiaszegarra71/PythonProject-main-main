from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registrar blueprints existentes
    from app.controllers.user_controller import user_bp
    from app.controllers.note_controller import note_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(note_bp, url_prefix='/api/notes')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Registrar blueprints NUEVOS (solo GET)
    from app.controllers.carrito_controller import carrito_bp
    from app.controllers.categoria_controller import categoria_bp
    from app.controllers.detalle_controller import detalle_bp
    from app.controllers.emprendimiento_controller import emprendimiento_bp
    from app.controllers.producto_controller import producto_bp
    from app.controllers.usuario_controller import usuario_bp

    app.register_blueprint(carrito_bp, url_prefix='/api/carritos')
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    app.register_blueprint(detalle_bp, url_prefix='/api/detalles')
    app.register_blueprint(emprendimiento_bp, url_prefix='/api/emprendimientos')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    app.register_blueprint(usuario_bp, url_prefix='/api/usuario')

    return app
