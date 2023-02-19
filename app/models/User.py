from model import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.CHAR(102), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
