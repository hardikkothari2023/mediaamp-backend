from datetime import date
from app.celery_worker import celery
from app import db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger

@celery.task
def load_daily_tasks():
    today = date.today()

     
    active_tasks = TaskManager.query.filter_by(status='active').all()

    added = 0
    for task in active_tasks:
         
        already_logged = TaskLogger.query.filter_by(task_id=task.id, log_date=today).first()
        if already_logged:
            continue

        log = TaskLogger(
            task_id=task.id,
            log_date=today,
            status_snapshot=task.status
        )
        db.session.add(log)
        added += 1

    db.session.commit()
    return f"{added} tasks logged for {today}"
