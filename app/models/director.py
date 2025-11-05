from extensions import db


class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    img_path = db.Column(db.String(512), nullable=True)

    def __repr__(self) -> str:
        return f"<Director {self.id} {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

