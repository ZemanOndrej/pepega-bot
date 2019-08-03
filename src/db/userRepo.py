from db.db import Session, EntityNotFound, User
from sqlalchemy import desc


def getUsers(count=20):
    ses = Session()
    return ses.query(User).order_by(desc(User.message_count)).limit(count)


def createUser(userId, name, ses=Session()):
    dbUser = getUserById(userId, ses)
    if dbUser is not None:
        return

    user = User(message_count=0, karma=0, name=name, id=userId)
    ses.add(user)
    ses.commit()


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


def createUsers(userList, ses=Session()):
    for u in userList:
        createUser(str(u.id), str(u), ses)


def getUserById(userId: str, session=Session()):
    return session.query(User).filter(User.id == userId).first()


def updateUserKarma(userId, val, ses=Session()):
    dbUser = getUserById(userId, ses)
    if dbUser is None:
        raise EntityNotFound("user not found")
    else:
        dbUser.karma += val

    ses.commit()
