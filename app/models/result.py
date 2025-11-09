from extensions import db
from datetime import datetime


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    meet_name = db.Column(db.String(200), nullable=False)
    meet_date = db.Column(db.Date, nullable=False)
    pdf_filename = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Result {self.id} {self.meet_name} ({self.meet_date})>"

    def to_dict(self):
        return {
            'id': self.id,
            'meet_name': self.meet_name,
            'meet_date': self.meet_date.isoformat() if self.meet_date else None,
            'pdf_filename': self.pdf_filename,
            'description': self.description,
        }

