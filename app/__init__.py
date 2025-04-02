from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # 🔹 Import models AFTER initializing db
    from app.models.user import User  # Ensure correct import path

    from app.routes import api_blueprint  # Import routes
    app.register_blueprint(api_blueprint)  # Register routes

    return app
