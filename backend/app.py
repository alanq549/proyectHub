from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object('backend.config.default.Config')

    # Initialize Extensions
    from backend.extensions.db import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from backend.extensions.jwt import jwt
    jwt.init_app(app)

    from backend.extensions.cors import cors
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    from backend.modules import modules_bp
    app.register_blueprint(modules_bp)

    @app.route('/')
    def index():
        return "Welcome to ProjectHub Backend!"

    return app
