from src.db.db import Session, Server, RoleReaction


def createServer(serverId: str, channelId: str):
    session = Session()
    server = Server(id=serverId, channel_id=channelId)
    session.add(server)
    session.commit()


def createRoleReaction(serverId: str, reaction: str, role: str):
    session = Session()
    roleReaction = RoleReaction(reaction=reaction, server_id=serverId, role=role)
    session.add(roleReaction)
    session.commit()


def getServerById(serverId: str):
    session = Session()
    return session.query(Server).filter(Server.id == serverId).first()


def getReactionRoleByServerAndReaction(serverId: str, reaction: str):
    session = Session()
    return session.query(RoleReaction).filter(serverId == RoleReaction.server_id,
                                              RoleReaction.reaction == reaction).first()
