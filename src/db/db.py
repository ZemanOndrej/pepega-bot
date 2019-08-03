from sqlalchemy.engine import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from util.params import getEnvVariable
from util.utilService import extractBoolFromString
import psycopg2
import time
import sys

DB_PORT = getEnvVariable("DB_PORT")
DB_USER = getEnvVariable("DB_USER")
DB_PW = getEnvVariable("DB_PW")
DB_DB = getEnvVariable("DB_DB")
DB_HOST = getEnvVariable("DB_HOST")
DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_DB}'
print(DB_URL)
Base = declarative_base()


class EntityNotFound(Exception):
    """Entity was not found"""
    pass


def getEngine():
    counter = 0
    counter_max = 20
    sleep_time = 5
    while counter < counter_max:
        try:
            counter += 1
            engine = create_engine(DB_URL)
            connection = engine.connect()
            print('connected to db successfully.')
            return engine
        except:
            time.sleep(sleep_time)
            if counter == counter_max:
                print(
                    f"db is unavailable for {counter_max * sleep_time} seconds, restart the application")
                sys.exit(1)
            else:
                print(
                    f"({counter}/20) db is unavailable, reconnecting to server in few seconds...")


def initDb():
    try:
        recreate = extractBoolFromString(getEnvVariable("RECREATE_DB"))
    except:
        recreate = False

    print(f"DB initialization recreate={recreate}")
    if recreate:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    message_count = Column(Integer)
    karma = Column(Integer)
    name = Column(String(50))


class Server(Base):
    __tablename__ = 'servers'
    id = Column(String, primary_key=True)
    role_reaction_channel_id = Column(String(50))
    prefix = Column(String(10))
    roleReactions = relationship(
        "RoleReaction", cascade="all,delete", backref='server', lazy='dynamic')
    karmaReaction = relationship(
        "KarmaReaction", cascade="all,delete", backref='server', lazy='dynamic')


class KarmaReaction(Base):
    __tablename__ = 'karma_reactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reaction = Column(String(50))
    karmaChange = Column(Integer)
    server_id = Column(String(50), ForeignKey('servers.id'))


class RoleReaction(Base):
    __tablename__ = 'role_reactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reaction = Column(String(50))
    role = Column(String(50))
    # server = relationship('Server')
    server_id = Column(String(50), ForeignKey('servers.id'))


engine = getEngine()
initDb()
Session = sessionmaker(bind=engine)
