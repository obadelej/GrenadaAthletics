from extensions import db


class Affiliate(db.Model):
    __tablename__ = 'affiliates'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(200), nullable=False)
    team_code = db.Column(db.String(50), nullable=False)
    team_colors = db.Column(db.String(200), nullable=True)
    img_path = db.Column(db.String(512), nullable=True)
    contact = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<Affiliate {self.id} {self.team_name}>"

