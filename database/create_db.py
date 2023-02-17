from database import Base, engine
from models import User, Projects


Base.metadata.create_all(bind=engine)
