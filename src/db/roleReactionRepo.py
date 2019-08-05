from db.db import Session, Server, RoleReaction, EntityNotFound
from db.serverRepo import getServerById


def createRoleReaction(serverId: str, reaction: str, role: str, ses=Session()):
    server = getServerById(serverId, ses)
    if server is None:
        raise EntityNotFound
    dbRR = ses.query(RoleReaction).filter(serverId == RoleReaction.server_id,
                                          RoleReaction.reaction == reaction, RoleReaction.role == role).first()
    if dbRR is not None:
        return False
    roleReaction = RoleReaction(
        reaction=reaction, server_id=serverId, role=role)
    ses.add(roleReaction)
    ses.commit()


def removeRoleReaction(serverId: str, reaction: str, ses=Session()):
    reaction = getRoleReactionByServerAndReaction(serverId, reaction, ses)
    ses.delete(reaction)
    ses.commit()


def getRoleReactionByServerAndReaction(serverId: str, reaction: str, ses=Session()):
    return ses.query(RoleReaction).filter(serverId == RoleReaction.server_id,
                                          RoleReaction.reaction == reaction).first()


def getRoleReactionByServer(serverId: str, ses=Session()):
    return ses.query(RoleReaction).filter(serverId == RoleReaction.server_id,).all()


def removeAllRoleReactions(serverId: str, ses=Session()):
    for r in getRoleReactionByServer(serverId, ses):
        ses.delete(r)
    ses.commit()
