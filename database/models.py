from database import Base
from sqlalchemy import Column, String, Integer, CHAR, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(CHAR(102), nullable=False)
    fullname = Column(String(50), nullable=False)
    user_type = Column(String(10), nullable=False)
    projects = relationship('projects', backref='author', lazy='dynamic')
    activies = relationship('activities', backref='activity', lazy='dynamic')


class Projects(Base):
    __tablename__= 'projects'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    company_name = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Activity(Base):
    __tablename__= 'activities'
    name = Column(String(20), primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


