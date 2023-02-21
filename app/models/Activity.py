from model import db


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    projects = db.Column(db.String(36), nullable=False)
