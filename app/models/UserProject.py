from model import db
import uuid



class UserProjects(db.Model):
    __tablename__ = 'userProjects' 
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
