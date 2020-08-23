from sqlalchemy import Table, Column, Integer, String, Binary, Date, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager


engine = create_engine('sqlite:///stats.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    race = Column(Integer)
    matchups = Column(Binary)
    children = relationship("Game")


class Map(Base):
    __tablename__ = 'map'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    children = relationship("Game")


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    map = Column(Integer, ForeignKey('map.id'))
    winner = Column(Integer, ForeignKey('player.id'))
    loser = Column(Integer, ForeignKey('player.id'))
    winner_race = Column(Integer, nullable=False)
    loser_race = Column(Integer, nullable=False)


@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base.metadata.create_all(engine)

