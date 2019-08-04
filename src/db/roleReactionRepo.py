from db.db import Session, Server, RoleReaction, EntityNotFound
from db.serverRepo import getServerById


def createRoleReaction(serverId: str, reaction: str, role: str,ses=Session()):
    server = getServerById(serverId, session)
    if server is None:
        raise EntityNotFound

    roleReaction = RoleReaction(
        reaction=reaction, server_id=serverId, role=role)
    session.add(roleReaction)
    session.commit()


def removeRoleReaction(serverId: str, reaction: str,ses=Session()):
    reaction = getRoleReactionByServerAndReaction(serverId, reaction, ses)
    ses.delete(reaction)
    ses.commit()


def getRoleReactionByServerAndReaction(serverId: str, reaction: str, ses=Session()):
    return ses.query(RoleReaction).filter(serverId == RoleReaction.server_id,
                                              RoleReaction.reaction == reaction).first()


def getRoleReactionByServer(serverId: str, ses=Session()):
    return ses.query(RoleReaction).filter(serverId == RoleReaction.server_id,).all()


def removeAllRoleReactions(serverId:str,ses=Session()):
    for r in getRoleReactionByServer(serverId,ses):
        ses.delete(r)
    ses.commit()
