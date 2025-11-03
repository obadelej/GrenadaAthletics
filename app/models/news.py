from datetime import datetime
from extensions import db


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.Text, nullable=False)
    photo_path = db.Column(db.String(512), nullable=True)

    def __repr__(self) -> str:
        return f"<News {self.id} {self.title}>"


