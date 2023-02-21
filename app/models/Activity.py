from model import db
import uuid


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)