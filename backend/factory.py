from flask import Flask
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object('config.default.Config')

    # Initialize Extensions
    from extensions.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Add database connection validation log
    with app.app_context():
        try:
            db.engine.connect()
            app.logger.info("Base de datos conectada exitosamente!")
        except Exception as e:
            app.logger.error(f"Error al conectar con la base de datos: {e}")

    from extensions.jwt import jwt
    jwt.init_app(app)

    from extensions.cors import cors
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    from modules import modules_bp
    app.register_blueprint(modules_bp)

    @app.route('/')
    def index():
        return "Bienvenido al Backend de ProjectHub!"

    return app
