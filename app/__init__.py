from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt  # ✅ Shared extensions
from flasgger import Swagger  # ✅ Import Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Swagger(app)  # ✅ Initialize Swagger

    # Import models so they're registered with SQLAlchemy
    from app.models import user, task_manager, task_logger

    # Register Blueprints
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
