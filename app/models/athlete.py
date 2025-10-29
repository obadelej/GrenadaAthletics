from extensions import db
from datetime import datetime

class Athlete(db.Model):
    """Athlete model"""
    __tablename__ = 'athletes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    personal_best = db.Column(db.String(100))
    achievements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Athlete {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sport': self.sport,
            'personal_best': self.personal_best,
            'achievements': self.achievements,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
