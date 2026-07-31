import os
from dotenv import load_dotenv
from factory import create_app
from extensions.db import db, migrate
from flask.cli import FlaskGroup

# Load environment variables from .env file
load_dotenv()

app = create_app()

# Initialize Flask-Migrate with the app and db
migrate.init_app(app, db)

# Create a FlaskGroup instance for command-line interface
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
