from model import db


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    comany_name = db.Column(db.String(20), nullable=False)
    user_project = db.Column(db.String(36), nullable=False)
    activities = db.Column(db.String(36), nullable=False)
