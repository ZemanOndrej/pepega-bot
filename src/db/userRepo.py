from db.db import Session, EntityNotFound, User
from sqlalchemy import desc


def getUsers(count=20):
    ses = Session()
    return ses.query(User).order_by(desc(User.message_count)).limit(count)


def incUserMsgCount(user):
    ses = Session()
    dbUser = getUserById(str(user.id), ses)

    if dbUser is None:
        dbUser = User(message_count=1, karma=0,
                      name=str(user), id=str(user.id))
        ses.add(dbUser)
    else:
        dbUser.message_count += 1

    ses.commit()


def getUserById(userId: str, session=Session()):
    return session.query(User).filter(User.id == userId).first()
