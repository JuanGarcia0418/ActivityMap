from database import Base, engine
from models import Flask_login


Base.metadata.create_all(bind=engine)
