from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # Initialize JWT

    # Import models AFTER initializing db
    from app.models.user import User

    # Import and register Blueprint
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
