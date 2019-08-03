
from db.db import Session, Server, KarmaEmote, EntityNotFound, User


def getKarmaEmoteByServerAndReaction(serverId: str, reaction: str, sess=Session()):
    return sess.query(KarmaEmote).filter(serverId == KarmaEmote.server_id,
                                         KarmaEmote.reaction == reaction).first()


def createKarmaEmote(serverId: str, reaction: str, change: int):
    session = Session()

    karmaEmote = KarmaEmote(
        reaction=reaction, server_id=serverId, karmaChange=change)
    session.add(karmaEmote)
    session.commit()
