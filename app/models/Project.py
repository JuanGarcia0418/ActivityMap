from model import db
import uuid

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(20), nullable=False)
    user_project = db.relationship('UserProjects', backref='viewProjects', lazy='dynamic')
    activities = db.relationship('Activity', backref='projects', lazy='dynamic')