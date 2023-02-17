from database import Base
from sqlalchemy import Column, String, Integer, CHAR, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='User'
    id = Column(Integer,primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(CHAR(102), nullable=False)
    fullname = Column(String(50), nullable=False)
    proyects = relationship('Projects', backref='User', lazy=True)


class Projects(Base):
    __tablename__= 'Projects'
    id = Column(Integer, primary_key=True, nullable=False)
    activityname = Column(String(20), nullable=False)
    resultactivity = Column(String(120), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

