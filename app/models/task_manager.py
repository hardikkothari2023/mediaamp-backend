from app.extensions import db
from datetime import datetime

class TaskManager(db.Model):
    __tablename__ = 'task_manager'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to TaskLogger
    logs = db.relationship('TaskLogger', backref='source_task', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return f"<TaskManager {self.title}>"
