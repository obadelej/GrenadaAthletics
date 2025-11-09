from extensions import db
from datetime import datetime


class Calendar(db.Model):
    __tablename__ = 'calendar'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    activity = db.Column(db.String(500), nullable=False)
    venue = db.Column(db.String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<Calendar {self.id} {self.activity} ({self.start_date} - {self.end_date})>"

    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'activity': self.activity,
            'venue': self.venue,
        }

