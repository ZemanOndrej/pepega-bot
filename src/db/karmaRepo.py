
from db.db import Session, Server, KarmaReaction, EntityNotFound, User


def getKarmaReactionByServerAndReaction(serverId: str, reaction: str, ses=Session()):
    return ses.query(KarmaReaction).filter(serverId == KarmaReaction.server_id,
                                           KarmaReaction.reaction == reaction).first()


def removeKarmaReaction(serverId: str, kr: str):
    ses = Session()
    kr = getKarmaReactionByServerAndReaction(serverId, kr, ses)
    ses.delete(kr)
    ses.commit()

def removeAllKarmaReactions(serverId:str,ses=Session()):
    for k in getKarmaReactionsByServer(serverId,ses):
        ses.delete(k)
    ses.commit()


def getKarmaReactionsByServer(serverId: str, ses=Session()):
    return ses.query(KarmaReaction).filter(serverId == KarmaReaction.server_id).all()


def saveKarmaReaction(serverId: str, reaction: str, change: int):
    session = Session()
    karmaReaction = getKarmaReactionByServerAndReaction(
        serverId, reaction, session)
    if karmaReaction is None:
        karmaReaction = KarmaReaction(
            reaction=reaction, server_id=serverId, karmaChange=change)
        session.add(karmaReaction)
    else:
        karmaReaction.karmaChange = change

    session.commit()
