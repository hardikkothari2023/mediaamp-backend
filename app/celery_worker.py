from celery import Celery
from app import create_app  
from app.config import Config
 
# Create Flask app instance
flask_app = create_app()
 
celery = Celery(
    flask_app.import_name,
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL   
)
 
celery.conf.update(flask_app.config)
 
# Ensure tasks run in Flask app context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
 
import tasks.daily_loader   
