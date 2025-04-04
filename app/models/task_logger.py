from app.extensions import db
from datetime import datetime

class TaskLogger(db.Model):
    __tablename__ = 'task_logger'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task_manager.id'), nullable=False, index=True)
    log_date = db.Column(db.Date, nullable=False)  # ✅ This is the column we'll filter by
    status_snapshot = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TaskLogger task_id={self.task_id} date={self.log_date}>"
