from database import Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, text

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
time = "%Y-%m-%dT%H:%M:%S.%f"

class Activity(Base):
    __tablename__='Activity'
    activity_id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String(16), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text(60), nullable=False)
    evidence = Column(String(32), nullable=False)
    projectid = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=False)
    imageid = Column(String(60), nullable=False)


    def __repr__(self):
        return f"<Activity {self.Name}>"
