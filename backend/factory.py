#factory.py
from flask import Flask, send_from_directory
import logging
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    factory_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(factory_dir, 'src')
    static_folder = os.path.join(src_path, 'static')

    app = Flask(
        __name__,
        static_folder=static_folder,
        static_url_path='/static'
    )

    app.config.from_object('src.config.default.Config')

    uploads_folder = os.path.join(static_folder, 'uploads')
    defaults_folder = os.path.join(static_folder, 'defaults')
    os.makedirs(uploads_folder, exist_ok=True)
    os.makedirs(defaults_folder, exist_ok=True)

    from extensions.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        try:
            db.engine.connect()
            app.logger.info("Base de datos conectada exitosamente!")
        except Exception as e:
            app.logger.error(f"Error al conectar con la base de datos: {e}")

    from extensions.jwt import jwt
    jwt.init_app(app)

    from extensions.cors import cors

    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        allowed_origins = [origin.strip() for origin in cors_origins_env.split(',')]
    else:
        allowed_origins = ["*"]

    # FIX CRÍTICO 3: Regex corregido para incluir /api y /api/v1
    cors.init_app(
        app,
        resources={r"/api(?:/v1)?/.*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Headers"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    from src.modules import modules_bp
    app.register_blueprint(modules_bp)

    @app.route('/static/uploads/<folder>/<filename>')
    def serve_upload(folder, filename):
        target_folder = os.path.join(uploads_folder, folder)
        return send_from_directory(target_folder, filename)

    @app.route('/static/defaults/<path:filename>')
    def serve_defaults(filename):
        return send_from_directory(defaults_folder, filename)

    @app.route('/')
    def index():
        return "Bienvenido al Backend de ProjectHub!"

    return app