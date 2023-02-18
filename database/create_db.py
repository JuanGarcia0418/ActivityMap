from database import Base, engine
from models import User, Projects, Activity


Base.metadata.create_all(bind=engine)
