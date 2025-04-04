from celery import Celery
from app import create_app  # Flask app factory
from app.config import Config

# Create Flask app instance
flask_app = create_app()

# Create Celery instance using Redis broker from Config
celery = Celery(
    flask_app.import_name,
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL  # Optional: for result backend
)

# Load config into Celery
celery.conf.update(flask_app.config)

# Ensure tasks run in Flask app context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# 👇 REGISTER the task module so Celery recognizes it
import tasks.daily_loader  # This ensures the task gets registered
