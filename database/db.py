from database import Session,engine
from models import Activity

local_session=Session(bind=engine)


def get_all_activities():
    return local_session.query(Activity).all()


def c_activity(activity_data):

    new_activity=Activity(**activity_data)

    try:
        local_session.add(new_activity)
        local_session.commit()

    except:
        local_session.rollback()
    finally:
        local_session.close()

