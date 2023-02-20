from database import Base
from sqlalchemy import Column, String, Integer, CHAR, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
import uuid



class User(Base):
    __tablename__ = 'user'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(CHAR(102), nullable=False)
    fullname = Column(String(50), nullable=False)
    user_type = Column(String(10), nullable=False)
    projects = relationship('projects', backref='author', lazy='dynamic')


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    company_name = Column(String(20), nullable=False)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    activities = relationship('activities', backref='projects', lazy='dynamic')

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)