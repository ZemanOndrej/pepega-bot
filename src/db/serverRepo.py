from db.db import Session, Server, EntityNotFound


def saveServer(serverId: str, channelId: str = None):
    session = Session()
    server = getServerById(serverId, session)
    if server is None:
        server = Server(id=serverId, role_reaction_channel_id=channelId)
        session.add(server)
    elif channelId is not None:
        setattr(server, 'role_reaction_channel_id', channelId)
    session.commit()


def getServerById(serverId: str, session=Session()):
    return session.query(Server).filter(Server.id == serverId).first()
