import os
from sqlalchemy.engine import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import psycopg2
import time

Base = declarative_base()


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)


DB_PORT = get_env_variable("DB_PORT")
DB_USER = get_env_variable("DB_USER")
DB_PW = get_env_variable("DB_PW")
DB_DB = get_env_variable("DB_DB")
DB_HOST = get_env_variable("DB_HOST")

DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PW}@{DB_HOST}/{DB_DB}'

counter = 0
counter_max = 20
sleep_time = 5

while counter < counter_max:
    try:
        counter += 1
        engine = create_engine(DB_URL)
        connection = engine.connect()
        print('connected to db successfully.')
    except:
        time.sleep(sleep_time)
        if counter == counter_max:
            print(
                f"db is unavailable for {counter_max * sleep_time} seconds, restart the application")
        else:
            print(
                f"({counter}/20) db is unavailable, reconnecting to server in few seconds...")
    else:
        break


class Server(Base):
    __tablename__ = 'servers'
    id = Column(String, primary_key=True)
    channel_id = Column(String(50))
    roleReactions = relationship(
        "RoleReaction", cascade="all,delete", backref='server', lazy='dynamic')


class RoleReaction(Base):
    __tablename__ = 'role_reactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reaction = Column(String(50))
    role = Column(String(50))
    # server = relationship('Server')
    server_id = Column(String(50), ForeignKey('servers.id'))


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
