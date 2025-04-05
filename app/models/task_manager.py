from app.extensions import db
from datetime import datetime

class TaskManager(db.Model):
    __tablename__ = 'task_manager'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_user = db.Column(db.String(255)) 

    
    logs = db.relationship('TaskLogger', backref='source_task', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return f"<TaskManager {self.title}>"
