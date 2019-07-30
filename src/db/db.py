import os
from sqlalchemy.engine import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         message = f"Expected environment variable '{name}' not set."
#         raise Exception(message)


# POSTGRES_URL = get_env_variable("POSTGRES_URL")
# POSTGRES_USER = get_env_variable("POSTGRES_USER")
# POSTGRES_PW = get_env_variable("POSTGRES_PW")
# POSTGRES_DB = get_env_variable("POSTGRES_DB")
POSTGRES_URL = 'localhost'
POSTGRES_USER = 'docker'
POSTGRES_PW = 'docker'
POSTGRES_DB = 'docker'

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'

engine = create_engine(DB_URL)
connection = engine.connect()


class Server(Base):
    __tablename__ = 'servers'
    id = Column(String, primary_key=True)
    channel_id = Column(String(50))
    roleReactions = relationship("RoleReaction", cascade="all,delete", backref='server', lazy='dynamic')


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
