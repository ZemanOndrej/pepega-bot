from db.db import Session, Server, RoleReaction, EntityNotFound
from db.serverRepo import getServerById


def createRoleReaction(serverId: str, reaction: str, role: str):
    session = Session()
    server = getServerById(serverId, session)
    if server is None:
        raise EntityNotFound

    roleReaction = RoleReaction(
        reaction=reaction, server_id=serverId, role=role)
    session.add(roleReaction)
    session.commit()


def removeRoleReaction(serverId: str, reaction: str):
    ses = Session()
    reaction = getReactionRoleByServerAndReaction(serverId, reaction, ses)
    ses.delete(reaction)
    ses.commit()


def getReactionRoleByServerAndReaction(serverId: str, reaction: str, session=Session()):
    return session.query(RoleReaction).filter(serverId == RoleReaction.server_id,
                                              RoleReaction.reaction == reaction).first()


def getReactionRoleByServer(serverId: str, session=Session()):
    return session.query(RoleReaction).filter(serverId == RoleReaction.server_id,).all()
