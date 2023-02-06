from database import Base, engine
from models import Activity


Base.metadata.create_all(bind=engine)
