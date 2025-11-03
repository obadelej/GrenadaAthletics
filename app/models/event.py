from extensions import db


class Event(db.Model):
    """Track and Field event definition"""
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(150), nullable=False)
    event_code = db.Column(db.String(50), nullable=False, unique=True)
    event_description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Event {self.event_code} {self.event_name}>'

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'event_code': self.event_code,
            'event_description': self.event_description,
        }
