from database import Base
from sqlalchemy import Column, String, Integer, CHAR

"""
Class Activity:
    ActivityId: int
    Name:text
    Description: text   
    Evidence: text
    ProjectId: int
    UserId: int
    ImageId: int

"""

class Flask_login(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(CHAR(102), nullable=False)
    fullname = Column(String(50), nullable=False)


    def __repr__(self):
        return f"<Flask_login {self.Name}>"
