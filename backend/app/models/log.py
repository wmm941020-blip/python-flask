from ..extensions import db
from datetime import datetime

class WorkLog(db.Model):
    __tablename__ = 'work_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    completion_status = db.Column(db.String(50)) # e.g., 'Completed', 'In Progress'
    issues = db.Column(db.Text)
    tomorrow_plan = db.Column(db.Text)
    rating = db.Column(db.Integer) # 1-5 or 1-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='work_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username,
            'date': self.date.isoformat(),
            'content': self.content,
            'completion_status': self.completion_status,
            'issues': self.issues,
            'tomorrow_plan': self.tomorrow_plan,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }
